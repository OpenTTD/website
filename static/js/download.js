
/**
 * Toggle whether the checksums must be shown or not.
 * @param self The "box" that is clicked on
 * @param id The id of the box with checksums
 */
function toggleChecksum(self, id)
{
	var obj = document.getElementById(id);
	if (obj.style.display == "block") {
		obj.style.display = "none";
		self.className = "checksums-dropdown"
	} else {
		obj.style.display = 'block';
		self.className = "checksums-dropdown-open"
	}
}

/**
 * Does the given base_name match any "files" in the data area?
 * @param base_name The name to search for.
 * @param data_area The area with data to search in.
 * @return true if and only if the area contains a name with the given base_name.
 */
function hasMatches(base_name, data_area)
{
	for (n = 0; n < data_area.childNodes.length; n++) {
		var node = data_area.childNodes[n];
		if (node.nodeType == 1 && node.id.match(base_name)) return true;
	}
	return false;
}

/**
 * Make a combobox for a specific level in the name's tree.
 * @param base The base name for all the ids.
 * @param level The depth this combobox is in.
 * @param base_name The name to "show".
 * @param prev_name How much of the name has already been shown.
 * @param data_area The area with data about possible states.
 * @param cur_state The current state of all combo boxes.
 */
function makeCombo(base, level, base_name, prev_name, data_area, cur_state)
{
	var html = '<select class="download-combo" id="' + base + '-' + level + '" onchange="updateCombo(this);">';

	/* Search for all the subtypes, we always have "any" as option. */
	var types = new Array();
	types[0] = base_name;

	/* Search for all the subtypes. */
	for (n = 0; n < data_area.childNodes.length; n++) {
		var node = data_area.childNodes[n];
		var name = node.id;
		if (node.nodeType == 1 && name.match(base_name)) {
			var subname = base_name + name.replace(base_name, "").replace(/-.*/, "").split('.', 2)[0];
			if (types[types.length - 1] != subname) {
				types[types.length] = subname;
			}
		}
	}

	/* Okay... only "any" is an option, so don't go deeper. */
	if (types.length == 1) return "";

	/* Add all subtypes we have */
	for (j = 0; j < types.length; j++) {
		type = types[j];
		var short_type = type.replace(prev_name, "");
		html += '<option ' + (cur_state.match(type) ? 'selected' : '') + ' value="' + type + '">' + (short_type == "" || short_type.match(/-$/) ? short_type + "any" : short_type) + '</option>';
	}
	html += '</select>';
	return html;
}

/**
 * Update the comboboxes based on the current state (remove some, add some, etc).
 * @param changed_combo The combobox initiating the state change.
 */
function updateCombo(changed_combo)
{
	var base =  changed_combo.id.replace(/-.*/, '');
	var combo_area = document.getElementById(base + "-combo");
	var data_area = document.getElementById(base + "-data");
	var base_name = document.getElementById(base + "-base-name").value;

	/* If the combo == the data area, then we start for the first time.
	 * In that case show as much as the detected user version, but do
	 * make sure it always shows at least one thing.
	 */
	var cur_state;
	if (changed_combo == data_area) {
		cur_state = document.getElementById(base + "-combo-state").value + "";
		while (!hasMatches(cur_state, data_area) && cur_state != "") {
			last = cur_state.lastIndexOf('-');
			cur_state = cur_state.substring(0, last);
		}
		if (cur_state + "-" == base_name) {
			cur_state = cur_state + "-";
		}
	} else {
		cur_state = changed_combo.value + "";
	}

	/* Recreate the two base data containers */
	var html = '';
	html += '<input type="hidden" id="' + base + '-combo-state" value="' + cur_state + '" />';
	html += '<input type="hidden" id="' + base + '-base-name" value="' + base_name +  '" />';

	var base_add = cur_state.replace(base_name, "").split("-");
	var prev_name = "";

	/* Create as many combos as needed */
	for (i = 0; i < base_add.length; i++) {
		var tmp = base_add[i];
		html += makeCombo(base, i, base_name, prev_name, data_area, cur_state);
		base_name += tmp + "-";
		prev_name = base_name;
	}
	html += makeCombo(base, base_add.length, base_name, prev_name, data_area, cur_state);
	combo_area.innerHTML = html;

	/* Hide all items that do not match the current 'show' state. */
	base_name = base_name.replace(/-$/, "");
	for (n = 0; n < data_area.childNodes.length; n++) {
		var node = data_area.childNodes[n];
		var name = node.id + "";
		if (node.nodeType == 1) {
			node.style.display = name.match(base_name) ? 'block' : 'none';
		}
	}
}

/**
 * Detect based on UserAgent what the best state would be.
 */
function detectByUA(state, base_name)
{
	detected = UAParser();

	switch (detected.os.name) {
		case "Windows":
			switch (detected.cpu.architecture) {
				case undefined:
				case "ia32":
					if (detected.os.version == "95" || detected.os.version == "98") {
						match = "windows-win9x";
					} else {
						match = "windows-win32";
					}
					break;
				case "amd64": match = "windows-win64"; break;
				default: match = "windows"; break;
			}
			break;

		case "Mac OS": match = "macos"; break;
		case "BeOS": match = "beos"; break;
		case "Morph OS": match = "morphos"; break;
		case "Debian": match = "linux-debian"; break;
		case "Ubuntu": match = "linux-ubuntu"; break;

		case "CentOS":
		case "Fedora":
		case "Gentoo":
		case "Mandriva":
		case "Linux":
		case "RedHat":
		case "Slackware":
			match = "linux"; break;

		default: match = ""; break;
	}

	state.value = base_name + match;
}
