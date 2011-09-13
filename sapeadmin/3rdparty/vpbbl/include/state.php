<?php

class phpMorphy_Link_Base {
	var $fsa;
	var $reader;
	var $trans;

	function phpMorphy_Link_Base(&$fsa, $trans) {
		$this->fsa =& $fsa;
		$this->reader =& $fsa->getReader();
		$this->trans = $trans;
	}

	function isAnnotation() { }
	function getTrans() { return $this->trans; }
	function &getFsa() { return $this->fsa; }
	function getPackedTrans() { return $this->reader->packTrans($this->trans); }
};

/**
 * This class represent "normal" link i.e. link that points to automat state
 */
class phpMorphy_Link extends phpMorphy_Link_Base {
	function isAnnotation() { return false; }

	function getDest() { return $this->trans['dest']; }
	function getAttr() { return $this->trans['attr']; }

	function &getTargetState() {
		$obj =& $this->_createState($this->getDest());
		return $obj;
	}

	function &_createState($index) {
		$obj =& new phpMorphy_State($this->fsa, $index);
		return $obj;
	}
}

class phpMorphy_Link_Annot extends phpMorphy_Link_Base {
	function isAnnotation() { return true; }

	function getAnnotationIndex() {
		return $this->reader->unpackAnnot($this->reader->packTrans($this->trans));
	}

	function getAnnotation() {
		return $this->fsa->getAnnot($this->getAnnotationIndex());
	}
};

class phpMorphy_State {
	var $fsa;
	var $transes;

	function phpMorphy_State(&$fsa, $index) {
		$this->fsa =& $fsa;

		$reader =& $fsa->getReader();
		$this->transes = $reader->unpackTranses($reader->readState($index));
	}

	function getLinks() {
		$result = array();

		foreach($this->transes as $trans) {
			if(!$trans['term']) {
				$result[] =& $this->_createNormalLink($trans);
			} else {
				$result[] =& $this->_createAnnotLink($trans);
			}
		}

		return $result;
	}

	function getSize() { return count($this->transes); }

	function &_createNormalLink($trans) {
		$obj =& new phpMorphy_Link($this->fsa, $trans);
		return $obj;
	}

	function &_createAnnotLink($trans) {
		$obj =& new phpMorphy_Link_Annot($this->fsa, $trans);
		return $obj;
	}
};
