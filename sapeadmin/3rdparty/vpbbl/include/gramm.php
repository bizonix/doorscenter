<?php


class phpMorphy_GramTab_ItemBuilder {
	function build($pos, $grammems) {
		if($pos) {
			return "$pos $grammems";
		} else {
			return $grammems;
		}
	}
};

class phpMorphy_GramTab {
	var $data;

	function phpMorphy_GramTab($fileName, &$builder) {
		$this->data = $this->_processRaw($this->_readFile($fileName), $builder);
	}

	function resolve($ancodes) {
		if($ancodes) {
			$result = array();
			foreach(str_split($ancodes, 2) as $ancode) {
				$result[] = $this->data[$ancode];
			}

			return $this->_joinItems($result);
		} else {
			return '';
		}
	}

	function _readFile($file) {
		if(false === ($data = unserialize(file_get_contents($file)))) {
			return php_morphy_error("Can`t read $file gramtab file");
		}

		return $data;
	}

	function _processRaw($data, &$builder) {
		$poses = $data['poses'];
		$grammems = $data['grammems'];

		$result = array();

		foreach($data['index'] as $ancode => $index) {
			$this->_splitIndex($index, $pos_idx, $gram_idx);
			$result[$ancode] = $builder->build($poses[$pos_idx], $grammems[$gram_idx]);
		}

		return $result;
	}

	function _splitIndex($index, &$posIdx, &$grammemsIdx) {
		$posIdx = $index & 0xFF;
		$grammemsIdx = $index >> 8;
	}

	function _joinItems($items) {
		return implode(';', $items);
	}
};
