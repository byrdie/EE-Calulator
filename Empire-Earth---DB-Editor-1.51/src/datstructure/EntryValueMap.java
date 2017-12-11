package datstructure;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import constants.EnumValue;
import constants.WorldID;

/**
 * Container class which hold the data returned by getValueMap();
 * @author MarcoForlini
 */
public class EntryValueMap{
	
	/** Map each value to the list of entries which use that value */
	public final Map<Object, List<Entry>> map;
	/** Map each not-null value to the list of entries which use that value */
	public final Map<Object, List<Entry>> mapClean;
	/** Total number of entries */
	public final int counter;

	/**
	 * Create a new {@link EntryValueMap}
	 * @param map		Map each value to the list of entries which use that value
	 * @param mapClean	Map each not-null value to the list of entries which use that value
	 * @param counter	Total number of entries
	 */
	public EntryValueMap (Map <Object, List<Entry>> map, Map <Object, List<Entry>> mapClean, int counter) {
		this.map = map;
		this.mapClean = mapClean;
		this.counter = counter;
	}
	
	/**
	 * Scan all entries and group entries by value
	 * @param entryGroups 			The list of entry groups
	 * @param index					Index of the field to read
	 * @param filterUndefined		If true, also create a second map which only contains fully defined entries
	 * @return an EntryValueMap		A new EntryValueMap which hold the results
	 */
	@SuppressWarnings ("null")
	public static EntryValueMap getValuesMap(List<EntryGroup> entryGroups, int index, boolean filterUndefined){
		Map<Object, List<Entry>> valueEntryMap = new HashMap<>();
		Map<Object, List<Entry>> valueEntryMapClean = new HashMap<>();
		DatStructure datStructure = entryGroups.get(0).datStructure;
		FieldStruct fieldStruct;
		if (index < datStructure.fieldStructs.length){
			fieldStruct = datStructure.fieldStructs[index];
		} else {
			fieldStruct = datStructure.extraField;
		}
		List<Entry> entries;
		Object value;
		int counter = 0;
		boolean enumType = fieldStruct.enumValues != null;
		EnumValue enum0 = enumType ? fieldStruct.enumValues[0] : null;
		boolean worldEnumType = enumType && enum0 instanceof WorldID;
		for (EntryGroup entryGroup : entryGroups){
			for (Entry entry : entryGroup){
				counter++;
				if (index < entry.size()){
					value = entry.get(index);
					if (value instanceof Link){
						value = ((Link) value).target;
					} else if (value instanceof Integer){
						if (enumType){
							int intVal = (Integer) value;
							value = enum0.parseValue(intVal);
							if (value == null){
								if (worldEnumType){
									continue;
								}
								throw new IllegalArgumentException("Can't find this code: " + intVal);
							}
						}
					}
					if (!valueEntryMap.containsKey(value)){
						entries = new ArrayList<>();
						entries.add(entry);
						valueEntryMap.put(value, entries);
					} else {
						valueEntryMap.get(value).add(entry);
					}
					
					if (filterUndefined && entry.isDefined()){
						if (!valueEntryMapClean.containsKey(value)){
							entries = new ArrayList<>();
							entries.add(entry);
							valueEntryMapClean.put(value, entries);
						} else {
							valueEntryMapClean.get(value).add(entry);
						}
					}
				}
			}
		}

		return new EntryValueMap (new TreeMap<>(valueEntryMap), new TreeMap<>(valueEntryMapClean), counter);
	}

}