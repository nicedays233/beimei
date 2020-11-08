package com.wyw.ingestion.common;

import org.apache.commons.lang.ArrayUtils;

public interface Parsable<T> {
	//check if the record is a header
	Boolean isHeader(String[] fields);
	//check if a record is valid
	Boolean isValid(String[] fields);

	//check if a record is empty
	// 检查字段的值是否为空
	default Boolean isEmpty(String[] fields, int[] indexes) {
		Boolean empty = false;
		//check
		if ( fields != null && fields.length > 0 ) {
			//loop
			for ( int i = 0; i < fields.length; i++ ) {
				//check
				if ( indexes != null && ArrayUtils.contains(indexes,  i) ) {
					//combine
					empty |= (fields[i] == null || fields[i].trim().length() <= 0);
				}
			}
		}
		return empty;
	}

	//parse the record
	T parse(String[] fields);
}
