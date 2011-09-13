<?php


if(!defined('PHPMORPHY_DIR')) define('PHPMORPHY_DIR', dirname(__FILE__));



class phpMorphy_GramInfo {
	var $fh;
	var $header;

	function phpMorphy_GramInfo($fileName) {
		if(false === ($fh = fopen($fileName, 'rb'))) {
			return php_morphy_error("Can`t open $fileName file");
		}

		$this->fh = $fh;
		if(false === ($this->header = $this->_readHeader($fh))) {
			return php_morphy_error("Can`t read morph data header");
		}

		if(false === $this->_validateHeader($this->header)) {
			return php_morphy_error("Invalid header in $fileName file");
		}
	}

	function readAncodes($gramHeader) {
		fseek($this->fh, $gramHeader['offset'] + 10 + $gramHeader['ancode_offset']);

		return explode(
			"\x0",
			fread(
				$this->fh,
				$gramHeader['size'] - $gramHeader['ancode_offset'] - 1
			)
		);
	}

	function readFlexiaData($gramHeader, $onlyBase = false) {
		fseek($this->fh, $gramHeader['offset'] + 10);
		return explode(
			"\x0",
			fread(
				$this->fh,
				$onlyBase ?
					$gramHeader['base_size'] - 1 :
					$gramHeader['ancode_offset'] - 1
			)
		);
	}

	function readGramInfoHeader($offset) {
		fseek($this->fh, $offset + 4);

		$result = unpack('vsize/vancode_offset/vbase_size', fread($this->fh, 6));
		$result['offset'] = $offset;

		return $result;
	}

	function getLanguage() {
		return $this->header['lang'];
	}

	function getCodepage() {
		return $this->header['codepage'];
	}

	function readAllGramInfoOffsets() {
		$fh = $this->fh;
		fseek($fh, 0x100);

		$result = array();
		for($offset = 0x100, $i = 0, $c = $this->header['flex_count']; $i < $c; $i++) {
			$result[] = $offset;

			$header = $this->readGramInfoHeader($offset);

			// skip padding
			$flexia_size = 10 + $header['size'];
			fseek($fh, $offset + $flexia_size);
			$pad_len = ord(fread($fh, 1));

			$offset += $flexia_size + $pad_len + 1;
		}

		return $result;
	}

	function _readHeader($fh) {
		fseek($fh, 0);

		$header = unpack(
			'Vver/Vis_be/Vflex_count/Vflex_offset/Vflex_size/',
			fread($fh, 20)
		);

		$len = ord(fread($fh, 1));
		$header['lang'] = rtrim(fread($fh, $len));

		$len = ord(fread($fh, 1));
		$header['codepage'] = rtrim(fread($fh, $len));

		return $header;
	}

	function _validateHeader($header) {
		if(
			1 != $header['ver'] &&
			0 == $header['is_be']
		) {
			return false;
		}

		return true;
	}
};

class phpMorphy_GramInfo_Decorator {
	var $info;

	function phpMorphy_GramInfo_Decorator(&$info) {
		$this->info =& $info;
	}

	function readAncodes($gramHeader) { return $this->info->readAncodes($gramHeader); }
	function readFlexiaData($gramHeader, $onlyBase = false) { return $this->info->readFlexiaData($gramHeader, $onlyBase); }
	function readGramInfoHeader($offset) { return $this->info->readGramInfoHeader($offset); }

	function getLanguage()  { return $this->info->getLanguage(); }
	function getCodepage()  { return $this->info->getCodepage(); }

	function readAllGramInfos(&$headers, &$flexias, &$ancodes) {
		return $this->info->readAllGramInfos($headers, $flexias, $ancodes);
	}
}

class phpMorphy_GramInfo_RuntimeCaching extends phpMorphy_GramInfo_Decorator {
	var $headers = array();
	var $base_flexia = array();
	var $all_flexia = array();
	var $ancodes = array();

	function readGramInfoHeader($offset) {
		if(!isset($this->headers[$offset])) {
			$this->headers[$offset] = $this->info->readGramInfoHeader($offset);
		}

		return $this->headers[$offset];
	}

	function readFlexiaData($gramHeader, $onlyBase = false)  {
		$offset = $gramHeader['offset'];

		if($onlyBase) {
			// This slow down!!
			/*
			if(empty($this->base_flexia[$offset])) {
				if(isset($this->all_flexia[$offset])) {
					$this->base_flexia[$offset] = array_slice($this->all_flexia[$offset], 0, 3);
				} else {
					$this->base_flexia[$offset] = $this->info->readFlexiaData($gramHeader, true);
				}
			}
			*/
			if(empty($this->base_flexia[$offset])) {
				$this->base_flexia[$offset] = $this->info->readFlexiaData($gramHeader, true);
			}

			return $this->base_flexia[$offset];
		} else {
			// This slow down!!
			/*
			if(!isset($this->all_flexia[$offset])) {
				$this->all_flexia[$offset] =& $this->info->readFlexiaData($gramHeader);
			}

			return $this->all_flexia[$offset];
			*/

			return $this->info->readFlexiaData($gramHeader, false);
		}
	}

	function readAncodes($gramHeader) {
		$offset = $gramHeader['offset'];

		if(!isset($this->gram_ids[$offset])) {
			$this->ancodes[$offset] = $this->info->readAncodes($gramHeader);
		}

		return $this->ancodes[$offset];
	}
}





class phpMorphy_Fsa_Reader {
	var $fh;
	var $annot_offset;
	var $annot_chunk_size;
	var $annot_length_fmt;
	var $annot_length_size;
	var $header;
	var $in_mem;
	var $data;

	function phpMorphy_Fsa_Reader($fh, $header = null, $inMem = false) {
		$this->fh = $fh;

		if(null == $header) {
			if(false === ($header = $this->readHeader($fh))) {
				return php_morphy_error("Can`t read header");
			}
		}

		if(!$this->validateHeader($header)) {
			return php_morphy_error("Invalid header format for current fsa reader");
		}

		$this->annot_offset = $header['annot_offset'];
		$this->header = $header;

		$this->annot_chunk_size = $header['annot_chunk_size'];
		$this->annot_length_size = $header['annot_size_len'];
		$this->annot_length_fmt = $this->_determineAnnotLengthFormat($header['annot_size_len']);

		$this->in_mem = $inMem;

		if($inMem) {
			$this->data = $this->_readFile($fh);

			$this->annot_offset -= 0x100;
			fclose($fh);
			$this->fh = null;
		}
	}

	function hasHash() {
		return $this->header['flags']['is_hash'];
	}

	function validateHeader($hdr) {
		if(
			'meal' != $hdr['fourcc'] ||
			1 != $hdr['ver']
		) {
			return php_morphy_error("Invalid fsa header");
		}

		return true;
	}

	function readHeader($fh) {
		fseek($fh, 0);

		$header = unpack(
			'a4fourcc/Vver/Vflags/Vchar_size/Vpadding_size/Vdest_size/Vhash_size/Vnodes_count/Vannot_size_len/Vannot_chunk_size/Vannot_chunks/Vannot_offset',
			fread($fh, 48)
		);

		if(false === $header) {
			return false;
		}

		$flags = array();
		$raw_flags = $header['flags'];
		$flags['is_tree'] =  $raw_flags & 0x01 ? true : false;
		$flags['is_hash'] =  $raw_flags & 0x02 ? true : false;
		$flags['is_be'] =  $raw_flags & 0x04 ? true : false;

		$header['flags'] = $flags;

		if(false === phpMorphy_Fsa_Reader::validateHeader($header)) {
			return php_morphy_error("Invalid header in fsa file");
		}

		return $header;
	}

	function readAnnot($index) {
		if($index) {
			$offset = $this->annot_offset + $index * $this->annot_chunk_size;

			if($this->in_mem) {
				list(, $len) = unpack(
					$this->annot_length_fmt,
					substr($this->data, $offset, $this->annot_length_size)
				);

				return substr(
					$this->data,
					$offset + $this->annot_length_size,
					$len
				);
			} else {
				$fh = $this->fh;
				fseek($fh, $offset);
				list(, $len) = unpack(
					$this->annot_length_fmt,
					fread($fh, $this->annot_length_size)
				);

				return fread($fh, $len);
			}
		} else {
			return null;
		}
	}

	function _determineAnnotLengthFormat($length) {
		if($this->header['flags']['is_be']) {
			$possible_fmts = array(
				1 => 'C',
				2 => 'n',
				4 => 'N'
			);
		} else {
			$possible_fmts = array(
				1 => 'C',
				2 => 'v',
				4 => 'V'
			);
		}

		if(!isset($possible_fmts[$length])) {
			return php_morphy_error("Unsupported annot_len_size given $length");
		}

		return $possible_fmts[$length];
	}

	function _readFile($fh) {
		$stat = fstat($fh);
		$size = $stat['size'] - 0x100;

		fseek($fh, 0x100);
		$data = fread($fh, $size);

		while(strlen($this->data) < $size && !feof($fh)) {
			$data .= fread($fh, 4096);
		}

		if(strlen($data) < $size) {
			return php_morphy_error("Can`t read fsa file");
		}

		return $data;
	}
}

class phpMorphy_Fsa_Reader_Factory {
	function &factory($fileName, $inMemory = false) {
		if(false === ($fh = fopen($fileName, 'rb'))) {
			return php_morphy_error("Can`t open $fileName fsa file");
		}

		if(false === ($header = phpMorphy_Fsa_Reader::readHeader($fh))) {
			return php_morphy_error("Can`t read header from $fileName fsa file");
		}

		if(false === ($readerClazz = phpMorphy_Fsa_Reader_Factory::_determineFsaClazzName($header, $inMemory))) {
			return php_morphy_error("Can`t determine fsa handler class");
		}

		if(!class_exists($readerClazz)) {
			return php_morphy_error("Class $readerClazz not exists, can`t read $fileName file");
		}

		$obj =& new $readerClazz($fh, $header, $inMemory);
		return $obj;
	}

	function _determineFsaClazzName($hdr, $inMemory) {
		$type = phpMorphy_Fsa_Reader_Factory::_getClazzNameForCaps($hdr);

		require_once(PHPMORPHY_DIR . '/' . $type . '.php');

		return 'phpMorphy_Fsa_Reader_' . $type;
	}

	function _getClazzNameForCaps($hdr) {
		if(!in_array($hdr['padding_size'], array(0, 3))) {
			php_morphy_error('Transition padding must be 0 or 3 bytes');
		}

		if($hdr['char_size'] != 1) {
			php_morphy_error('Attribute size must be 1 bytes long');
		}

		if(!in_array($hdr['dest_size'], array(3, 4))) {
			php_morphy_error('Dest size must be 3 to 4 bytes long');
		}

		if(!in_array($hdr['annot_chunk_size'], array(1, 2, 4))) {
			php_morphy_error('Annot chunk size must be 1, 2 or 4 bytes long');
		}

		$flags = $hdr['flags'];
		return
			($hdr['dest_size'] == 3 ? 'S' : 'L') .
			($flags['is_tree'] ? 'T' : 'S') .
			($flags['is_be'] ? 'BE' : 'LE') .
			($flags['is_hash'] ? 'WH' : 'NH') .
			($hdr['padding_size'] == 3 ? 'WP' : 'NP');
	}
};


class phpMorphy_Fsa {
	var $root_trans;
	var $annot_decoder;
	var $reader;

	function phpMorphy_Fsa(&$reader, &$annotDecoder) {
		$this->reader =& $reader;
		$this->annot_decoder = $annotDecoder;
		$this->root_trans = $reader->readTrans(0);
	}

	function getRootTrans() { return $this->root_trans; }

	function &getReader() { return $this->reader; }

	function &getRootState() {
		$obj =& $this->_createState(0);
		return $obj;
	}

	function getAnnot($annotIndex) {
		return $this->annot_decoder->decode($this->reader->readAnnot($annotIndex));
	}

	function getAnnotByTrans($rawTrans) {
		$reader =& $this->reader;

		return $this->getAnnot(
			$reader->unpackAnnot($reader->readTrans($reader->extractDest($rawTrans)))
		);
	}

	function walk($startTrans, $word, $readAnnot = true) {
		$trans = $startTrans;
		$reader =& $this->reader;

		for($i = 0, $c = strlen($word); $i < $c; $i++) {
			$prev_trans = $trans;

			$result = $reader->findCharInState(
				$reader->extractDest($trans),
				ord($word[$i]),
				$trans
			);

			if(!$result) {
				$trans = $prev_trans;
				break;
			}
		}

		$annot = null;
		$result = false;

		if($i >= $c) {
			$result = true;

			if($readAnnot) {
				$annot = $this->getAnnot(
					$reader->unpackAnnot($reader->readTrans($reader->extractDest($trans)))
				);
			}
		}

		return array(
			'result' => $result,
			'last_trans' => $trans,
			'walked' => $i,
			'annot' => $annot
		);
	}

	function collect($startNode, $callback, $readAnnot = true, $path = '') {
		$total = 0;
		$reader =& $this->getReader();

		$stack = array();
		$stack_idx = array();
		$start_idx = 0;
		array_push($stack, null);
		array_push($stack_idx, null);

		$state = $reader->readState($reader->extractDest($startNode));

		do {
			for($i = $start_idx, $c = count($state); $i < $c; $i++) {
				$trans = $state[$i];

				if($reader->extractTerm($trans)) {
					$total++;

					if($readAnnot) {
						$annot = $this->getAnnot($reader->unpackAnnot($trans));
					} else {
						$annot = $trans;
					}

					if(!call_user_func($callback, $path, $annot)) {
						return $total;
					}
				} else {
					$char = chr($reader->extractAttr($trans));

					$path .= $char;
					array_push($stack, $state);
					array_push($stack_idx, $i + 1);
					$state = $reader->readState($reader->extractDest($trans));
					$start_idx = 0;

					break;
				}
			}

			if($i >= $c) {
				$state = array_pop($stack);
				$start_idx = array_pop($stack_idx);
				$path = substr($path, 0, -1);
			}
		} while(!empty($stack));

		return $total;
	}

	function &_createState($index) {
		require_once(PHPMORPHY_DIR . '/fsa_state.php');

		$obj =& new phpMorphy_State($this, $index);
		return $obj;
	}
};

class phpMorphy_Fsa_Decorator {
	var $fsa;

	function phpMorphy_Fsa_Decorator(&$fsa) {
		$this->fsa =& $fsa;
	}

	function getRootTrans() { return $this->fsa->getRootTrans(); }
	function &getReader() { return $this->fsa->getReader(); }
	function &getRootState() { return $this->fsa->getRootState(); }
	function getAnnot($index) { return $this->fsa->getAnnot($index); }
	function getAnnotByTrans($trans) { return $this->fsa->getAnnotByTrans($trans); }
	function walk($start, $word, $readAnnot = true) { return $this->fsa->walk($start, $word, $readAnnot); }
	function collect($start, $callback, $readAnnot = true, $path = '') { return $this->fsa->collect($start, $callback, $readAnnot, $path); }
};


class phpMorphy_Fsa_Cache_Builder {
	var $fsa;
	var $max_level;
	var $cache;
	var $cache_trans;

	function phpMorphy_Fsa_Cache_Builder(&$fsa, $maxLevel) {
		$this->fsa =& $fsa;
		$this->max_level = $maxLevel;

		if(false === $this->_buildCache()) {
			return php_morphy_error("Can`t build cache");
		}
	}

	function getMaxLevel() { return $this->max_level; }
	function getCache() { return $this->cache; }
	function getLastTransesCache() { return $this->cache_trans; }

	function __sleep() {
		return array('max_level', 'cache');
	}

	function _buildCache() {
		$state =& $this->fsa->getRootState();

		$links = $state->getLinks();

		if(count($links) != 1) {
			return php_morphy_error("Invalid root state");
		}

		$link =& $links[0];

		if($link->isAnnotation()) {
			return php_morphy_error("Invalid root state");
		}

		// enum states
		$this->cache = array();

		$this->_enum(
			$link->getTargetState(),
			1,
			'',
			$link->getPackedTrans()
		);

		return true;
	}

	function _enum(&$state, $cur_level, $path, $prev_trans) {
		$links = $state->getLinks();

		for($i = 0; $i < count($links); $i++) {
			$link =& $links[$i];

			if(!$link->isAnnotation()) {
				$future_path = $path . chr($link->getAttr());
				$packed_trans = $link->getPackedTrans();

				if($cur_level >= $this->max_level) {
					$this->cache[$future_path] = $packed_trans;
				} else {
					$this->_enum(
						$link->getTargetState(),
						$cur_level + 1,
						$future_path,
						$packed_trans
					);
				}
			} else {
				$this->cache[$path] = $link->getAnnotation();
				$this->cache_trans[$path] = $prev_trans;
			}
		}
	}
};

class phpMorphy_Fsa_Cache extends phpMorphy_Fsa_Decorator {
	var $root_trans;
	var $max_level;
	var $cache;
	var $cache_trans;

	function phpMorphy_Fsa_Cache(&$fsa, &$builder) {
		parent::phpMorphy_Fsa_Decorator($fsa);

		$this->root_trans = $fsa->getRootTrans();
		$this->max_level = $builder->getMaxLevel();
		$this->cache = $builder->getCache();
		$this->cache_trans = $builder->getLastTransesCache();
	}

	function walk($startTrans, $word, $readAnnot = true) {
		if($startTrans != $this->root_trans) {
			return $this->fsa->walk($startTrans, $word, $readAnnot);
		}

		$w = substr($word, 0, $this->max_level);

		if(isset($this->cache[$w])) {
			$cache = $this->cache[$w];

			if(is_int($cache)) {
				$left = substr($word, $this->max_level);

				$result = $this->fsa->walk($cache, $left, $readAnnot);

				$result['walked'] += $this->max_level;

				return $result;
			} else {
				return array(
					'result' => true,
					'last_trans' => $this->cache_trans[$w],
					'walked' => strlen($word),
					'annot' => $cache
				);
			}
		}

		return $this->fsa->walk($this->root_trans, $word, $readAnnot);
	}
};

class phpMorphy_Fsa_WordsCollector {
	var $items = array();
	var $limit;

	function phpMorphy_Fsa_WordsCollector($collectLimit) {
		$this->limit = $collectLimit;
	}

	function collect($word, $annot) {
		if(count($this->items) < $this->limit) {
			$this->items[$word] = $annot;
			return true;
		} else {
			return false;
		}
	}

	function getItems() { return $this->items; }
	function clear() { $this->items = array(); }
	function getCallback() { return array(&$this, 'collect'); }
};



class phpMorphy_Morphier_Base {
	var $graminfo;
	var $fsa;
	var $root_trans;

	function phpMorphy_Morphier_Base(&$fsa, &$graminfo) {
		$this->fsa =& $fsa;
		$this->graminfo =& $graminfo;
		$this->root_trans = $fsa->getRootTrans();
	}

	function &_createWordDescriptor($word, $annots) {
		$obj =& new phpMorphy_WordDescriptor($word, $annots, $this->graminfo);
		return $obj;
	}

	function &getFsa() { return $this->fsa; }
	function &getGramInfo() { return $this->graminfo; }
};

class phpMorphy_Morphier_Dictionary extends phpMorphy_Morphier_Base {
	function &morph($word) {
		$result = $this->fsa->walk($this->root_trans, $word);

		if(!$result['result'] || !is_array($result['annot'])) {
			$result = false;
			return $result;
		}

		return $this->_createWordDescriptor($word, $result['annot']);
	}
};

class phpMorphy_Morphier_PredictBySuffix extends phpMorphy_Morphier_Base {
	var $min_suf_len;

	function phpMorphy_Morphier_PredictBySuffix(&$fsa, &$graminfo, $minimalSuffixLength = 4) {
		parent::phpMorphy_Morphier_Base($fsa, $graminfo);

		$this->min_suf_len = $minimalSuffixLength;
	}

	function &morph($word) {
		$word_len = strlen($word);

		for($i = 1, $c = $word_len - $this->min_suf_len; $i < $c; $i++) {
			$result = $this->fsa->walk($this->root_trans, substr($word, $i));

			if($result['result'] && is_array($result['annot'])) {
				break;
			}
		}

		if($i < $c) {
			$known_len = $word_len - $i;
			$unknown_len = $i;

			$this->_fixAnnots($result['annot'], $unknown_len);

			return $this->_createWordDescriptor($word, $result['annot']);
		} else {
			$result = false;

			return $result;
		}
	}

	function _fixAnnots(&$annots, $unknownLen) {
		for($i = 0, $c = count($annots); $i < $c; $i++) {
			$annots[$i]['cplen'] = $unknownLen;
		}
	}
};

class phpMorphy_PredictMorphier_Collector extends phpMorphy_Fsa_WordsCollector {
	var $used_poses = array();
	var $collected = 0;

	function collect($path, $annots) {
		if($this->collected > $this->limit) {
			return false;
		}

		$used_poses =& $this->used_poses;

		for($i = 0, $c = count($annots); $i < $c; $i++) {
			$annot = $annots[$i];
			$annot['cplen'] = $annot['plen'] = 0;

			$pos_id = $annot['pos_id'];

			if(isset($used_poses[$pos_id])) {
				$result_idx = $used_poses[$pos_id];

				if($annot['freq'] > $this->items[$result_idx]['freq']) {
					$this->items[$result_idx] = $annot;
				}
			} else {
				$used_poses[$pos_id] = count($this->items);
				$this->items[] = $annot;
			}
		}

		$this->collected++;
		return true;
	}

	function clear() {
		parent::clear();
		$this->collected = 0;
		$this->used_poses = array();
	}
};

class phpMorphy_Morphier_PredictByDatabse extends phpMorphy_Morphier_Base {
	var $collector;
	var $min_postfix_match;

	function phpMorphy_Morphier_PredictByDatabse(&$fsa, &$graminfo, $minPostfixMatch = 2, $collectLimit = 32) {
		parent::phpMorphy_Morphier_Base($fsa, $graminfo);

		$this->min_postfix_match = $minPostfixMatch;
		$this->collector =& $this->_createCollector($collectLimit);
	}

	function &morph($word) {
		$result = $this->fsa->walk($this->root_trans, strrev($word));

		if($result['result'] && is_array($result['annot'])) {
			$annots = $result['annot'];
		} else {
			if(null === ($annots = $this->_determineAnnots($result['last_trans'], $result['walked']))) {
				$result = false;
				return $result;
			}
		}

		$this->_fixAnnots($annots);

		return $this->_createWordDescriptor($word, $annots);
	}

	function _determineAnnots($trans, $matchLen) {
		$annots = $this->fsa->getAnnotByTrans($trans);

		if(null == $annots && $matchLen >= $this->min_postfix_match) {
			$this->collector->clear();

			$this->fsa->collect(
				$trans,
				$this->collector->getCallback()
			);

			$annots = $this->collector->getItems();
		}

		return $annots;
	}

	function _fixAnnots(&$annots) {
		for($i = 0, $c = count($annots); $i < $c; $i++) {
			$annots[$i]['cplen'] = $annots[$i]['plen'] = 0;
		}
	}

	function &_createCollector($limit) {
		$obj =& new phpMorphy_PredictMorphier_Collector($limit);
		return $obj;
	}
};

class phpMorphy_Morphier_Decorator {
	var $morphier;

	function phpMorphy_Morphier_Decorator(&$morphier) {
		$this->morphier = $morphier;
	}

	function &morph($word) { return $this->morphier->morph($word); }
}

class phpMorphy_Morphier_WithGramTab extends phpMorphy_Morphier_Decorator {
	var $gramtab;
	var $file_name;

	function phpMorphy_Morphier_WithGramTab(&$morphier, $gramtabFile) {
		parent::phpMorphy_Morphier_Decorator($morphier);
		$this->file_name = $gramtabFile;
	}

	function &morph($word) {
		$result =& $this->morphier->morph($word);

		if(false !== $result) {
			$result =& new phpMorphy_WordDescriptorWithGramtab($result, $this->_getGramTab());
		}

		return $result;
	}

	function &_getGramTab() {
		if(!isset($this->gramtab)) {
			require_once(PHPMORPHY_DIR . '/gramm.php');
			$this->gramtab =& new phpMorphy_GramTab($this->file_name, $this->_createBuilder());
		}

		return $this->gramtab;
	}

	function &_createBuilder() {
		$obj =& new phpMorphy_GramTab_ItemBuilder();
		return $obj;
	}
};

class phpMorphy_Morphier_Chain {
	var $morphiers = array();

	function getMorphiers() { return $this->morphiers; }
	function add(&$morphier) { $this->morphiers[] =& $morphier; }

	function &morph($word) {
		$result = false;

		for($i = 0, $c = count($this->morphiers); false == $result && $i < $c; $i++) {
			$result =& $this->morphiers[$i]->morph($word);
		}

		return $result;
	}
};


class phpMorphy_CommonAnnotDecoder {
	function decode($annotation) {
		if(strlen($annotation) < 9) {
			return null;
		}

		$result = array();

		foreach(str_split($annotation, 9) as $data) {
			$result[] = unpack('Voffset/a2ancode/Cflen/Cplen/Ccplen', $data);
		}

		return $result;
	}
};

class phpMorphy_PredictAnnotDecoder {
	function decode($annotation) {
		if(strlen($annotation) < 10) {
			return null;
		}

		$result = array();

		foreach(str_split($annotation, 10) as $data) {
			$result[] = unpack('Voffset/vfreq/a2ancode/Cflen/Cpos_id', $data);
		}

		return $result;
	}
};

class phpMorphy_WordDescriptor {
	var $gram_headers;
	var $offsets;
	var $prefixes;
	var $bases;
	var $ancodes;
	var $graminfo;
	var $word;

	function phpMorphy_WordDescriptor($word, $annotAry, &$gramInfo) {
		$this->graminfo =& $gramInfo;
		$this->word = $word;

		$this->bases = array();
		$this->ancodes = array();
		$this->prefixes = array();
		$this->offsets = array();

		if(!is_array($annotAry)) {
			return php_morphy_error("Invalid annot given");
		}

		foreach($annotAry as $annot) {
			$this->offsets[] = $annot['offset'];

			$flen = $annot['flen'];

			if($flen) {
				$this->bases[] = substr($word, $annot['cplen'] + $annot['plen'], -$flen);
			} else {
				$this->bases[] = substr($word, $annot['cplen'] + $annot['plen']);
			}

			// common prefix len
			$this->prefixes[] = substr($word, 0, $annot['cplen']);
			$this->ancodes[] = $annot['ancode'];
		}
	}

	function getWord() { return $this->word; }
	function getPseudoRoot() { return array_unique($this->bases); }
	function getTotalInterpretations() { return count($this->bases); }

	function getBaseForm() {
		$this->_readGramInfoHeaders();
		$result = array();

		for($i = 0, $c = count($this->gram_headers); $i < $c; $i++) {
			$this->_generateWordFormsInKey(
				$this->prefixes[$i],
				$this->bases[$i],
				$this->graminfo->readFlexiaData($this->gram_headers[$i], true),
				$result
			);
		}

		return array_keys($result);
	}

	function getAllForms() {
		$this->_readGramInfoHeaders();
		$result = array();

		for($i = 0, $c = count($this->gram_headers); $i < $c; $i++) {
			$this->_generateWordFormsInKey(
				$this->prefixes[$i],
				$this->bases[$i],
				$this->graminfo->readFlexiaData($this->gram_headers[$i]),
				$result
			);
		}

		return array_keys($result);
	}

	function getAllFormsWithGramInfo() {
		$this->_readGramInfoHeaders();
		$result = array();

		for($i = 0, $c = count($this->gram_headers); $i < $c; $i++) {
			$forms = array();
			$this->_generateWordFormsInKey(
				$this->prefixes[$i],
				$this->bases[$i],
				$this->graminfo->readFlexiaData($this->gram_headers[$i]),
				$forms
			);

			$result[] = array(
				'forms' => array_keys($forms),
				'common' => $this->ancodes[$i],
				'all' => $this->_getAncodes($this->gram_headers[$i])
			);
		}

		return $result;
	}

	function _readGramInfoHeaders() {
		if(!isset($this->gram_headers)) {
			$this->gram_headers = array();
			$graminfo =& $this->graminfo;

			foreach($this->offsets as $offset) {
				$this->gram_headers[] = $graminfo->readGramInfoHeader($offset);
			}

			unset($this->offsets);
		}
	}

	function _getAncodes($header) {
		return $this->graminfo->readAncodes($header);
	}

	function _generateWordForms($prefix, $base, $flexias, &$result) {
		for($i = 0, $c = count($flexias); $i < $c; $i += 2) {
			$result[] = $prefix . $flexias[$i] . $base . $flexias[$i + 1];
		}
	}

	function _generateWordFormsInKey($prefix, $base, $flexias, &$result) {
		for($i = 0, $c = count($flexias); $i < $c; $i += 2) {
			$result[$prefix . $flexias[$i] . $base . $flexias[$i + 1]] = 1;
		}
	}
};

class phpMorphy_WordDescriptor_Decorator {
	var $desc;

	function phpMorphy_WordDescriptor_Decorator(&$descriptor) {
		$this->desc =& $descriptor;
	}

	function getTotalInterpretations() { return $this->desc->getTotalInterpretations(); }
	function getPseudoRoot() { return $this->desc->getPseudoRoot(); }
	function getWord() { return $this->desc->getWord(); }
	function getBaseForm() { return $this->desc->getBaseForm(); }
	function getAllForms() { return $this->desc->getAllForms(); }
	function getAllFormsWithGramInfo() { return $this->desc->getAllFormsWithGramInfo(); }
};

class phpMorphy_WordDescriptorWithGramtab extends phpMorphy_WordDescriptor_Decorator {
	var $gramtab;

	function phpMorphy_WordDescriptorWithGramtab(&$desc, &$gramtab) {
		parent::phpMorphy_WordDescriptor_Decorator($desc);
		$this->gramtab =& $gramtab;
	}

	function getAllFormsWithGramInfo() {
		$result = $this->desc->getAllFormsWithGramInfo();

		for($i = 0, $c = count($result); $i < $c; $i++) {
			$res =& $result[$i];
			$res['common'] = $this->gramtab->resolve($res['common']);

			$res2 =& $res['all'];
			for($j = 0, $jc = count($res2); $j < $jc; $j++) {
				$res2[$j] = $this->gramtab->resolve($res2[$j]);
			}
		}

		return $result;
	}
};

if(version_compare(PHP_VERSION, '5') < 0) {


function php_morphy_error($errorMessage, $result = false) {
	trigger_error($errorMessage, E_USER_ERROR);
	return $result;
}

// from pear::compat
// str_split()

/**
 * Replace str_split()
 *
 * @category    PHP
 * @package     PHP_Compat
 * @link        http://php.net/function.str_split
 * @author      Aidan Lister <aidan@php.net>
 * @version     $Revision: 1.9 $
 * @since       PHP 5
 * @require     PHP 4.0.1 (trigger_error)
 */
if (!function_exists('str_split'))
{
    function str_split ($string, $split_length = 1)
    {
        if (!is_numeric($split_length)) {
            trigger_error('str_split() expects parameter 2 to be long, ' . gettype($split_length) . ' given', E_USER_WARNING);
            return false;
        }

        if ($split_length < 1) {
            trigger_error('str_split() The the length of each segment must be greater then zero', E_USER_WARNING);
            return false;
        }

        preg_match_all('/.{1,' . $split_length . '}/s', $string, $matches);
        return $matches[0];
    }
}

// file_put_contents()

if (!defined('FILE_USE_INCLUDE_PATH')) {
    define('FILE_USE_INCLUDE_PATH', 1);
}

if (!defined('FILE_APPEND')) {
    define('FILE_APPEND', 8);
}


/**
 * Replace file_put_contents()
 *
 * @category    PHP
 * @package     PHP_Compat
 * @link        http://php.net/function.file_put_contents
 * @author      Aidan Lister <aidan@php.net>
 * @version     $Revision: 1.19 $
 * @internal    $resource_context is not supported
 * @since       PHP 5
 * @require     PHP 4.0.1 (trigger_error)
 */
if (!function_exists('file_put_contents'))
{
    function file_put_contents ($filename, $content, $flags = null, $resource_context = null)
    {
        // If $content is an array, convert it to a string
        if (is_array($content)) {
            $content = implode('', $content);
        }

        // If we don't have a string, throw an error
        if (!is_string($content)) {
            trigger_error('file_put_contents() The 2nd parameter should be either a string or an array', E_USER_WARNING);
            return false;
        }

        // Get the length of date to write
        $length = strlen($content);

        // Check what mode we are using
        $mode = ($flags & FILE_APPEND) ?
                    $mode = 'a' :
                    $mode = 'w';

        // Check if we're using the include path
        $use_inc_path = ($flags & FILE_USE_INCLUDE_PATH) ?
                    true :
                    false;

        // Open the file for writing
        if (($fh = @fopen($filename, $mode, $use_inc_path)) === false) {
            trigger_error('file_put_contents() failed to open stream: Permission denied', E_USER_WARNING);
            return false;
        }

        // Write to the file
        $bytes = 0;
        if (($bytes = @fwrite($fh, $content)) === false) {
            $errormsg = sprintf('file_put_contents() Failed to write %d bytes to %s',
                            $length,
                            $filename);
            trigger_error($errormsg, E_USER_WARNING);
            return false;
        }

        // Close the handle
        @fclose($fh);

        // Check all the data was written
        if ($bytes != $length) {
            $errormsg = sprintf('file_put_contents() Only %d of %d bytes written, possibly out of free disk space.',
                            $bytes,
                            $length);
            trigger_error($errormsg, E_USER_WARNING);
            return false;
        }

        // Return length
        return $bytes;
    }
}

if (!function_exists('file_get_contents'))
{
    function file_get_contents ($filename, $incpath = false, $resource_context = null)
    {
        if (false === $fh = fopen($filename, 'rb', $incpath)) {
            trigger_error('file_get_contents() failed to open stream: No such file or directory', E_USER_WARNING);
            return false;
        }

        clearstatcache();
        if ($fsize = filesize($filename)) {
            $data = fread($fh, $fsize);
        }

        else {
            while (!feof($fh)) {
                $data .= fread($fh, 8192);
            }
        }

        fclose($fh);

        return $data;
    }
}

} else {

class phpMorphy_Exception extends Exception { };

function php_morphy_error($errorMessage, $result = false) {
	throw new phpMorphy_Exception($errorMessage);
}

}

class phpMorphy_FilesBundle {
	 var $dir;
	 var $lang;
	function phpMorphy_FilesBundle() {
		$this->dir = dirname(__FILE__)."/";
		$this->lang = 'rus';
	}

	function getCommonAutomatFile() {
		return $this->_genFileName('%s/common_aut.%s.bin');
	}

	function getPredictAutomatFile() {
		return $this->_genFileName('%s/predict_aut.%s.bin');
	}

	function getGramInfoFile() {
		return $this->_genFileName('%s/morph_data.%s.bin');
	}

	function getGramTabFile() {
		return $this->_genFileName('%s/gramtab.%s.bin');
	}

	function _genFileName($fmt) {
		return sprintf($fmt, $this->dir, strtolower($this->lang));
	}

};

class phpMorphy_FsaCreator {
	var $cache_levels;
	var $cache_dir;

	function phpMorphy_FsaCreator($cacheLevels, $cacheDir) {
		$this->cache_levels = $cacheLevels;
		$this->cache_dir = $cacheDir;
	}

	function &create($fileName, &$reader, &$decoder) {
		$fsa =& $this->_createFsa($reader, $decoder);

		if($this->cache_levels) {
			return $this->_createFsaCache($fileName, $fsa);
		} else {
			return $fsa;
		}
	}

	function &_createFsa(&$reader, &$decoder) {
		$obj =& new phpMorphy_Fsa($reader, $decoder);
		return $obj;
	}

	function &_createFsaCache($fileName, &$fsa) {
		$obj =& new phpMorphy_Fsa_Cache(
			$fsa,
			$this->_createCacheBuilder($fileName, $fsa)
		);

		return $obj;
	}

	function &_createCacheBuilder($fileName, &$fsa) {
		// TODO: Use external caching interface
		if($this->cache_dir) {
			$file_name = $this->_buildCacheFileName($fileName);

			if(!file_exists($file_name)) {
				// TODO: what returns file_put_contents() on error(FALSE or 0)?
				file_put_contents(
					$file_name,
					serialize(
						new phpMorphy_Fsa_Cache_Builder($fsa, $this->cache_levels)
					)
				);
			}

			$result =& unserialize(file_get_contents($file_name));
			if(false === $result) {
				$result = php_morphy_error("Can`t read fsa cache file $file_name");
			}

			return $result;
		} else {
			$obj =& new phpMorphy_Fsa_Cache_Builder($fsa, $this->cache_levels);
			return $obj;
		}
	}

	function _buildCacheFileName($fileName) {
		return $this->cache_dir . DIRECTORY_SEPARATOR . basename($fileName) . '.cache';
	}
};

class phpMorphy {
	var $morphier;

	/**
	 * Options structure:
	 * array(
	 * 	in_memory => true|false,
	 * 	fsa_cache_levels => int,
	 * 	fsa_cache_dir => string(empty string for disable),
	 * 	graminfo_cache => true|fale,
	 * 	with_gramtab => true|false,
	 * 	predict_by_suffix => true|false,
	 * 	predict_by_suffix_min_suffix_len => int,
	 * 	predict_by_db => true|false,
	 * 	predict_by_db_min_postfix_match => int,
	 *	predict_by_db_max_collect_items => int
	 * )
	 */
	function phpMorphy(&$bundle, $options = null) {
		$options = array(
		'in_memory' => false, // загружать словарь в память(скорость поиска увеличивается примерно на 25%)
		'graminfo_cache' => true, // включить кэш для грам. информации(рекомендуется включать всегда)
		'fsa_cache_levels' => 0, // кол-во уровней для кэширования дерева(0 - выключить кэширование). рекомендуемые значения: 2-3
		'fsa_cache_dir' => '', // директория где будет лежать кэш. дерева('' - выключить).
		'with_gramtab' => true, // включить преобразование анкодов в человекочитаемую форму
		'predict_by_suffix' => true,  // включить предсказание по суффиксу(уменьшает скорость)
		'predict_by_db' => true // включить предсказание по предварительно обсчитанной базе(уменьшает скорость)
	);
		$options = $this->_repairOptions($options);
		$in_mem = $options['in_memory'];

		$fsa_creator =& $this->_createFsaCreator(
			$options['fsa_cache_levels'],
			$options['fsa_cache_dir']
		);

		$common_fsa =& $fsa_creator->create(
			$bundle->getCommonAutomatFile(),
			$this->_createFsaReader($bundle->getCommonAutomatFile(), $in_mem),
			$this->_createCommonAnnotDecoder()
		);

		$graminfo =& $this->_createGramInfo(
			$bundle->getGramInfoFile(),
			$options['graminfo_cache']
		);

		$std_morphier =& $this->_createStandartMorphier($common_fsa, $graminfo);

		if($options['predict_by_suffix']) {
			$suf_morphier =& $this->_createPredictBySuffixMorphier(
				$common_fsa,
				$graminfo,
				$options['predict_by_suffix_min_suffix_len']
			);
		}

		if($options['predict_by_db']) {
			$db_morphier =& $this->_createPredictByDatabaseMorphier(
				$fsa_creator->create(
					$bundle->getPredictAutomatFile(),
					$this->_createFsaReader($bundle->getPredictAutomatFile(), $in_mem),
					$this->_createPredictAnnotDecoder()
				),
				$graminfo,
				$options['predict_by_db_min_postfix_match'],
				$options['predict_by_db_max_collect_items']
			);
		}

		// create chain
		if(!$options['predict_by_suffix'] && !$options['predict_by_db']) {
			if($options['with_gramtab']) {
				$this->morphier =& new phpMorphy_Morphier_WithGramTab(
					$std_morphier,
					$bundle->getGramTabFile()
				);
			} else {
				$this->morphier =& $std_morphier;
			}
		} else {
			$this->morphier =& $this->_createChainMorphier();

			if($options['with_gramtab']) {
				$file = $bundle->getGramTabFile();
				$this->morphier->add(new phpMorphy_Morphier_WithGramTab($std_morphier, $file));

				if($options['predict_by_suffix']) {
					$this->morphier->add(new phpMorphy_Morphier_WithGramTab($suf_morphier, $file));
				}

				if($options['predict_by_db']) {
					$this->morphier->add(new phpMorphy_Morphier_WithGramTab($db_morphier, $file));
				}
			} else {
				$this->morphier->add($std_morphier);

				if($options['predict_by_suffix']) {
					$this->morphier->add($suf_morphier);
				}

				if($options['predict_by_db']) {
					$this->morphier->add($db_morphier);
				}
			}
		}
	}

	function &getMorphier() { return $this->morphier; }

	function &morph($word) { return $this->morphier->morph($word); }

	function _repairOptions($options) {
		$default = array(
		 	'in_memory' => false,
 			'fsa_cache_levels' => null,
			'fsa_cache_dir' => null,
			'graminfo_cache' => true,
			'with_gramtab' => false,
			'predict_by_suffix' => false,
			'predict_by_suffix_min_suffix_len' => null,
			'predict_by_db' => false,
			'predict_by_db_min_postfix_match' => null,
			'predict_by_db_max_collect_items' => null
		);

		$result = array();
		settype($options, 'array');

		foreach($default as $k => $v) {
			if(array_key_exists($k, $options)) {
				$result[$k] = $options[$k];
			} else {
				$result[$k] = $v;
			}
		}

		return $result;
	}

	function &_createGramInfo($file, $cacheType) {
		$obj =& new phpMorphy_GramInfo($file);

		if($cacheType) {
			$obj =& new phpMorphy_GramInfo_RuntimeCaching($obj);
		}

		return $obj;
	}

	function &_createFsaCreator($cacheLevel, $cacheDir) {
		$obj =& new phpMorphy_FsaCreator($cacheLevel, $cacheDir);
		return $obj;
	}

	function &_createFsa(&$reader, &$decoder) {
		$obj =& new phpMorphy_Fsa($reader, $decoder);
		return $obj;
	}

	function &_createFsaReader($fileName, $inMemory) {
		$obj =& phpMorphy_Fsa_Reader_Factory::factory($fileName, $inMemory);
		return $obj;
	}

	function &_createCommonAnnotDecoder() {
		$obj =& new phpMorphy_CommonAnnotDecoder();
		return $obj;
	}

	function &_createPredictAnnotDecoder() {
		$obj =& new phpMorphy_PredictAnnotDecoder();
		return $obj;
	}

	function &_createChainMorphier() {
		$obj =& new phpMorphy_Morphier_Chain();
		return $obj;
	}

	function &_createStandartMorphier(&$fsa, &$graminfo) {
		$obj =& new phpMorphy_Morphier_Dictionary($fsa, $graminfo);
		return $obj;
	}

	function &_createPredictBySuffixMorphier(&$fsa, &$graminfo, $len) {
		if(isset($len)) {
			$obj =& new phpMorphy_Morphier_PredictBySuffix($fsa, $graminfo, $len);
		} else {
			$obj =& new phpMorphy_Morphier_PredictBySuffix($fsa, $graminfo);
		}

		return $obj;
	}

	function &_createPredictByDatabaseMorphier(&$fsa, &$graminfo, $minMatch, $maxItems) {
		if(isset($minLen) && isset($maxItems)) {
			$obj =& new phpMorphy_Morphier_PredictByDatabse($fsa, $graminfo, $minMatch, $maxItems);
		} else {
			$obj =& new phpMorphy_Morphier_PredictByDatabse($fsa, $graminfo);
		}

		return $obj;
	}
};
