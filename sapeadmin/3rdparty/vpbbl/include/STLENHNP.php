<?php


class phpMorphy_Fsa_Reader_STLENHNP extends phpMorphy_Fsa_Reader {
	function getStream() { return $this->fh; }

	function unpackTranses($rawTranses) {
		settype($rawTranses, 'array');
		$result = array();

		foreach($rawTranses as $rawTrans) {
			$result[] = array(
				'term'	=> $rawTrans & 0x0100 ? true : false,
				'llast'	=> $rawTrans & 0x0200 ? true : false,
				'rlast'	=> $rawTrans & 0x0400 ? true : false,
				'attr'	=> $rawTrans & 0xFF,
				'dest'	=> $rawTrans >> 11,
			);
		}

		return $result;
	}

	function packTrans($trans) {
		$result = 0;

		// term
		if($trans['term']) $result |= 0x0100;
		// llast
		if($trans['llast']) $result |= 0x0200;
		// rlast
		if($trans['rlast']) $result |= 0x0400;
		// attr
		$result |= (int)$trans['attr'] & 0xFF;
		// dest
		$result |= (int)$trans['dest'] << 11;

		return $result;
	}

	function extractDest($rawTrans) { return $rawTrans >> 11; }
	function extractAttr($rawTrans) { return $rawTrans & 0xFF; }
	function extractTerm($rawTrans) { return $rawTrans & 0x0100; }

	function unpackAnnot($rawTrans) {
		if($rawTrans & 0x0100) {
			return (($rawTrans & 0xFF) << 21) | ($rawTrans >> 11);
		} else {
			return 0;
		}
	}

	function _readRootTrans() {
		return $this->readTrans(0, false);
	}

	function readState($index) {
		$in_mem = $this->in_mem;

		if($in_mem) {
			$index <<= 2;
		} else {
			$fh = $this->fh;
		}

		$result = array();

		if($in_mem) {
			list(, $trans) = unpack('V', substr($this->data, $index, 4));
			$index += 4;
		} else {
			fseek($fh, 0x100 + ($index << 2));
			list(, $trans) = unpack('V', fread($fh, 4));
		}

		if(($trans & 0x0100) && !($trans & 0x0200 || $trans & 0x0400)) {
			$result[] = $trans;

			if($in_mem) {
				list(, $trans) = unpack('V', substr($this->data, $index, 4));
				$index += 4;
			} else {
				list(, $trans) = unpack('V', fread($fh, 4));
			}
		}

		for($expect = 1; $expect; $expect--) {
			if(0 == ($trans & 0x0200)) $expect++;
			if(0 == ($trans & 0x0400)) $expect++;

			$result[] = $trans;

			if($expect > 1) {
				if($in_mem) {
					list(, $trans) = unpack('V', substr($this->data, $index, 4));
					$index += 4;
				} else {
					list(, $trans) = unpack('V', fread($fh, 4));
				}
			}
		}

		return $result;
	}

	function readTrans($index) {
		if($this->in_mem) {
			list(, $trans) = unpack('V', substr($this->data, $index << 2, 4));
		} else {
			fseek($this->fh, 0x100 + ($index << 2));
			list(, $trans) = unpack('V', fread($this->fh, 4));
		}

		return $trans;
	}

	function findCharInState($stateIdx, $char, &$lastTrans) {
		$found = false;

		$fh = $this->fh;
		$data = $this->data;
		$in_mem = $this->in_mem;

		if($in_mem) {
			list(, $trans) = unpack('V', substr($data, $stateIdx << 2, 4));
		} else {
			fseek($fh, 0x100 + ($stateIdx << 2));
			list(, $trans) = unpack('V', fread($fh, 4));
		}

		// If first trans is term(i.e. pointing to annot) then skip it
		if($trans & 0x0100) {
			// When this is single transition in state then break
			if($trans & 0x0200 && $trans & 0x0400) {
				$lastTrans = $trans;
				return false;
			}

			$stateIdx++;

			if($in_mem) {
				list(, $trans) = unpack('V', substr($data, $stateIdx << 2, 4));
			} else {
				fseek($fh, 0x100 + ($stateIdx << 2));
				list(, $trans) = unpack('V', fread($fh, 4));
			}
		}

		$attr = $trans & 0xFF;

		// walk through state
		for($idx = 1, $j = 0;;) {
			if($attr == $char) {
				$found = true;
				break;
			} else if($attr > $char) {
				if($trans & 0x0200) {
					break;
				}
				$idx = $idx << 1;
			} else {
				if($trans & 0x0400) {
					break;
				}

				$idx = ($idx << 1) + 1;
			}

			if($j > 255) {
				return php_morphy_error('Infinite recursion possible');
			}
			$j++;

			// read next node in tree
			$offset = ($stateIdx + $idx - 1) << 2;

			if($in_mem) {
				list(, $trans) = unpack('V', substr($data, $offset, 4));
			} else {
				fseek($fh, 0x100 + $offset);
				list(, $trans) = unpack('V', fread($fh, 4));
			}

			$attr = $trans & 0xFF;
		}

		if($found) {
			$lastTrans = $trans;
		}

		return $found;
	}
};
