from pathlib import Path
import json
import copy
import re

from mdutils import MdUtils


def read_json_file(json_file: Path) -> dict:
    with open(json_file, "r", encoding="utf-8") as file_pointer:
        contents = json.load(file_pointer)
    return contents


def replace_and_lowercase(text: str, replace: str = " ", repalce_with="_") -> str:
    return text.lower().replace(replace, repalce_with)


def get_md_file_from_title(title: str, export_folder: Path) -> MdUtils:
    file_name = f"{replace_and_lowercase(title)}.md"
    file_path = export_folder / file_name
    return MdUtils(file_name=str(file_path))


def add_link_to_json_schema(md_file: MdUtils, link: str):
    name = link.split("/")[-1] + ".schema.json"
    md_file.new_line("Defined in: " + md_file.new_inline_link(link=link, text=name))


def get_hyperlinked_object_text(title: str, md_file: MdUtils):
    item_type = replace_and_lowercase(title)
    return md_file.new_inline_link(link=f"{item_type}.md", text=item_type)


def get_cross_file_ppty_link(parent: str, child: str, md_file: MdUtils):
    parent = replace_and_lowercase(parent)
    child = replace_and_lowercase(child)
    return md_file.new_inline_link(link=f"{parent}.md/#{child}", text=child)


def get_type_for_property(ppty_content: dict) -> str:
    if "enum" in ppty_content:
        return "enum"
    if "type" in ppty_content:
        return ppty_content.get("type")
    if "const" in ppty_content:
        return ppty_content.get("const")
    if "oneOf" in ppty_content:
        return " | ".join([get_type_for_property(oneof) for oneof in ppty_content.get("oneOf")])
    if "properties" in ppty_content:
        return "object"
    return "unknown"


def get_ppty_type(ppty_dict: dict, md_file: MdUtils):
    ppty_type = get_type_for_property(ppty_dict)
    if ppty_type in ["object", "array"]:
        ppty_type = get_hyperlinked_object_text(ppty_dict.get("title"), md_file)
    else:
        ppty_type = f"`{ppty_type}`"
    return ppty_type


def get_inline_link(ppty: str, md_file: MdUtils):
    return md_file.new_inline_link(link=f"#{ppty}", text=ppty)


def add_table_of_properties(contents: dict, md_file: MdUtils):
    list_of_strings = ["Property", "Type", "Required", "Format", "Title"]
    md_file.new_line()
    for ppty, ppty_dict in contents["properties"].items():
        format = ppty_dict.get("format", "")
        list_of_strings.extend(
            [
                get_inline_link(ppty, md_file),
                get_ppty_type(ppty_dict, md_file),
                ":white_check_mark:" if ppty in contents.get("required", []) else "",
                f"`{format}`" if format else "",
                ppty_dict.get("title") or "",
            ]
        )
    md_file.new_line()
    md_file.new_table(
        columns=5,
        rows=len(contents["properties"]) + 1,
        text=list_of_strings,
        text_align="center",
    )


def handle_enums(enums: list[str], md_file: MdUtils):
    list_of_texts = ["Value"] + [f"`{el}`" for el in enums]
    md_file.new_line()
    md_file.new_table(columns=1, rows=len(list_of_texts), text=list_of_texts, text_align="left")


def handle_inline_constraints(ppty_dict: dict, md_file: MdUtils):
    constraints = {
        "minLength": "Minimum Length",
        "maxLength": "Maximum Length",
        "multipleOf": "Must be multiple of",
        "minimum": "Minimum Number",
        "maximum": "Maximum Number",
        "exclusiveMinimum": "Exclusive Minimum",
        "pattern": "Regex Pattern",
        "$comment": "Comment",
        "uniqueItems": "Items should be unique",
        "minItems": "Minimum number of items",
        "const": "Constant",
    }

    for key, label in constraints.items():
        if key in ppty_dict:
            if key in ["$comment"]:
                md_file.new_line(f"{label}: {ppty_dict[key]}")
            else:
                md_file.new_line(f"{label}: `{ppty_dict[key]}`")


def add_ppty_details(contents: dict, md_file: MdUtils):
    for ppty, ppty_dict in contents["properties"].items():
        md_file.new_header(level=2, title=ppty, add_table_of_contents="n")
        md_file.new_line()
        md_file.write(ppty_dict.get("description", ""))
        md_file.new_line()
        md_file.new_line()
        md_file.new_list(
            [
                "is required" if ppty in contents.get("required", []) else "is not required",
                f"Type: {get_ppty_type(ppty_dict, md_file)}",
            ]
        )
        if "enum" in ppty_dict:
            handle_enums(ppty_dict["enum"], md_file)
        if "oneOf" in ppty_dict:
            md_file.new_header(level=4, title="One Of", add_table_of_contents="n")
            for oneof in ppty_dict.get("oneOf"):
                if "enum" in oneof:
                    handle_enums(oneof["enum"], md_file)
                handle_inline_constraints(oneof, md_file)
                md_file.new_line()
        if "anyOf" in ppty_dict:
            md_file.new_header(level=4, title="Any Of", add_table_of_contents="n")
            for anyof in ppty_dict.get("anyOf"):
                if "enum" in anyof:
                    handle_enums(anyof["enum"], md_file)
                handle_inline_constraints(anyof, md_file)
                md_file.new_line()
        handle_inline_constraints(ppty_dict, md_file)


def check_if_mutually_exclusive_requirement_exists(oneof: dict):
    return True if "required" in oneof and "not" in oneof and "required" in oneof["not"] else False


def generate_mutually_exlcusive_requirement_table(oneofs: list[dict], md_file: MdUtils):
    one_ofs_with_exclusive_required = [
        item for item in oneofs if check_if_mutually_exclusive_requirement_exists(item)
    ]
    if not one_ofs_with_exclusive_required:
        return

    md_file.new_line()
    md_file.new_header(level=3, title="Mutual Exclusivity Requirement", add_table_of_contents="n")
    list_of_strings = ["`if` present", "should `not` be present"]
    for item in one_ofs_with_exclusive_required:
        list_of_strings.extend(
            [
                " ".join([f"{get_inline_link(el, md_file)}" for el in item["required"]]),
                " ".join([f"{get_inline_link(el, md_file)}" for el in item["not"]["required"]]),
            ]
        )
    md_file.new_line()
    md_file.new_table(
        columns=2,
        rows=len(one_ofs_with_exclusive_required) + 1,
        text=list_of_strings,
        text_align="left",
    )


def handle_oneofs(
    oneofs: list[dict], md_file: MdUtils, export_folder: Path, breadcrums: list[str]
):
    md_file.new_header(level=2, title="One Of", add_table_of_contents="n")
    md_file.new_line()
    for one_of_item in oneofs:
        if "properties" in one_of_item:
            md_file.new_line(get_hyperlinked_object_text(one_of_item.get("title"), md_file))
            generate_markdown_for_object(one_of_item, export_folder, copy.deepcopy(breadcrums))
        if one_of_item.get("type") == "array":
            generate_markdown_for_object(one_of_item, export_folder, copy.deepcopy(breadcrums))
    generate_mutually_exlcusive_requirement_table(oneofs, md_file)


def handle_anyofs(
    anyofs: list[dict], md_file: MdUtils, export_folder: Path, breadcrums: list[str]
):
    md_file.new_header(level=2, title="Any Of", add_table_of_contents="n")
    md_file.new_line()
    for any_of_item in anyofs:
        if "properties" in any_of_item:
            md_file.new_line(get_hyperlinked_object_text(any_of_item.get("title"), md_file))
            generate_markdown_for_object(any_of_item, export_folder, copy.deepcopy(breadcrums))
        elif any_of_item.get("type") == "array":
            generate_markdown_for_object(any_of_item, export_folder, copy.deepcopy(breadcrums))
        elif "required" in any_of_item:
            for req_item in any_of_item["required"]:
                md_file.new_line(get_inline_link(req_item, md_file))


def check_if_conditional_validation(content: dict) -> bool:
    return {"if", "then"}.issubset(content) or {"not"}.issubset(content)


def get_if_property_text(
    key: str,
    value: dict,
    md_file: MdUtils,
    export_folder: Path,
    not_: bool = False,
    parent: str = "",
    breadcrums: list = [],
) -> str:
    inline_link = (
        get_hyperlinked_object_text(key, md_file)
        if not parent
        else get_cross_file_ppty_link(parent, key, md_file)
    )
    if "const" in value:
        middle_text = "is not" if not_ else "is"
        return f"{inline_link} {middle_text} `{value['const']}`"
    elif "enum" in value:
        middle_text = "is not" if not_ else "is"
        enum_text = ", ".join([f"`{el}`" for el in value["enum"]])
        return f"{inline_link} {middle_text} one of [{enum_text}]"
    elif "contains" in value:
        middle_text = "does not" if not_ else ""
        generate_markdown_for_object(
            value.get("contains"), export_folder, copy.deepcopy(breadcrums)
        )
        return f"{inline_link} {middle_text} contain " + get_hyperlinked_object_text(
            value["contains"].get("title"), md_file
        )
    elif "exclusiveMinimum" in value:
        middle_text = "has not" if not_ else "has"
        return (
            f"{inline_link} {middle_text} exclusive minimum value of `{value['exclusiveMinimum']}`"
        )
    elif "not" in value:
        return get_if_property_text(
            key,
            value["not"],
            md_file,
            export_folder,
            not not_,
            breadcrums=copy.deepcopy(breadcrums),
        )
    elif ("minimum" in value) or ("maximum" in value):
        middle_text = "is not" if not_ else "is"
        min_text = f"minimum value of `{value['minimum']}`" if "minimum" in value else ""
        max_text = f"maximum value of `{value['maximum']}`" if "maximum" in value else ""
        return f"{inline_link} {middle_text} {min_text}, {max_text}"
    elif "required" in value:
        verb = "are" if len(value["required"]) > 1 else "is"
        middle_text = "not present" if not_ else "present"
        return f"{', '.join([get_cross_file_ppty_link(key, el, md_file) for el in value['required']])} {verb} {middle_text} in {inline_link}"
    elif "properties" in value:
        middle_text = "has no key/s" if not_ else "has key/s "
        generate_markdown_for_object(value, export_folder, copy.deepcopy(breadcrums))
        return f"{inline_link} {middle_text}" + get_hyperlinked_object_text(
            value.get("title"), md_file
        )
    elif "pattern" in value:
        middle_text = "does not" if not_ else ""
        return f"{inline_link} {middle_text} match pattern `{value['pattern']}`"
    elif "maxItems" in value:
        middle_text = "is not" if not_ else "is"
        return f"Number of items in {inline_link} {middle_text} less than or equal to `{value['maxItems']}`"
    else:
        raise Exception(f"{key=}, {value=}")


def get_if_properties_text(
    if_content: dict,
    md_file: MdUtils,
    export_folder: Path,
    not_: bool = False,
    parent="",
    breadcrums: list = [],
):
    if_present_texts = []
    for key, value in if_content["properties"].items():
        if "properties" in value:
            key_text = get_hyperlinked_object_text(key, md_file)
            ppty_text = get_if_condition_text(
                value, md_file, export_folder, not_, key, breadcrums=copy.deepcopy(breadcrums)
            )
            if_present_texts.append(f"{key_text}.{ppty_text}")
        else:
            if_present_texts.append(
                get_if_property_text(
                    key,
                    value,
                    md_file,
                    export_folder,
                    not_,
                    parent,
                    breadcrums=copy.deepcopy(breadcrums),
                )
            )
    return " AND ".join(if_present_texts)


def get_if_condition_text(
    if_content: dict,
    md_file: MdUtils,
    export_folder: Path,
    not_: bool = False,
    parent: str = "",
    breadcrums: list = [],
) -> str:
    if_present_text = ""
    if "not" in if_content:
        if_present_text += get_if_condition_text(
            if_content["not"],
            md_file,
            export_folder,
            not_=True,
            breadcrums=copy.deepcopy(breadcrums),
        )
    if "properties" in if_content:
        if_present_text += get_if_properties_text(
            if_content,
            md_file,
            export_folder,
            not_=not_,
            parent=parent,
            breadcrums=copy.deepcopy(breadcrums),
        )

    if "oneOf" in if_content:
        oneof_texts = []
        for oneof in if_content["oneOf"]:
            oneof_texts.append(
                get_if_condition_text(
                    oneof, md_file, export_folder, breadcrums=copy.deepcopy(breadcrums)
                )
            )
        if_present_text += "<br><br> XOR <br><br>".join(oneof_texts)

    if "anyOf" in if_content:
        anyof_texts = []
        for anyof in if_content["anyOf"]:
            anyof_texts.append(
                get_if_condition_text(
                    anyof, md_file, export_folder, breadcrums=copy.deepcopy(breadcrums)
                )
            )
        if_present_text += "<br><br> OR <br><br>".join(anyof_texts)

    if "allOf" in if_content:
        allof_texts = []
        for allof in if_content["allOf"]:
            allof_texts.append(
                get_if_condition_text(
                    allof, md_file, export_folder, breadcrums=copy.deepcopy(breadcrums)
                )
            )
        if_present_text += "<br><br> AND <br><br>".join(allof_texts)

    if "required" in if_content and not if_present_text:
        reqs = [get_inline_link(el, md_file) for el in if_content["required"]]
        if_present_text = ",".join(reqs) + (" exists" if len(reqs) == 1 else " exist")
    return if_present_text


def get_then_not_text(then_not_content: list[dict], md_file: MdUtils) -> str:
    then_not_text = ""
    if "required" in then_not_content:
        then_not_text += ", ".join(
            [f"{get_inline_link(el, md_file)}" for el in then_not_content["required"]]
        )
        plural = len(then_not_content["required"]) > 1

    if "anyOf" in then_not_content:
        all_req_items = [
            ppt for subitem in then_not_content["anyOf"] for ppt in subitem["required"]
        ]
        then_not_text += ", ".join([f"{get_inline_link(el, md_file)}" for el in all_req_items])
        plural = len(all_req_items) > 1
    return then_not_text + (" are not present" if plural else " is not present")


def get_conditional_table_record(
    conditional_content: dict,
    md_file: MdUtils,
    export_folder: Path,
    prev_if_text: str = "",
    breadcrums: list = [],
):
    conditional_records = []
    if_text = (
        get_if_condition_text(
            conditional_content["if"], md_file, export_folder, breadcrums=copy.deepcopy(breadcrums)
        )
        if "if" in conditional_content
        else ""
    )
    if prev_if_text:
        if_text = f"{prev_if_text} AND {if_text}"
    if "then" in conditional_content and "if" in conditional_content["then"]:
        conditional_records.extend(
            get_conditional_table_record(
                conditional_content["then"],
                md_file,
                export_folder,
                prev_if_text=if_text,
                breadcrums=copy.deepcopy(breadcrums),
            )
        )
    if "then" in conditional_content and "allOf" in conditional_content["then"]:
        then_not_text, then_text = "", []
        for all_of_item in conditional_content["then"]["allOf"]:
            if "if" in all_of_item:
                conditional_records.extend(
                    get_conditional_table_record(
                        all_of_item,
                        md_file,
                        export_folder,
                        prev_if_text=if_text,
                        breadcrums=copy.deepcopy(breadcrums),
                    )
                )
            else:
                then_text.extend(
                    [f"{get_inline_link(el, md_file)}" for el in all_of_item.get("required", [])]
                )
                then_not_text += (
                    get_then_not_text(all_of_item["not"], md_file) + "<br>"
                    if "not" in all_of_item
                    else ""
                )
        then_text = (
            ", ".join(then_text) + (" are present" if len(then_text) > 1 else " is present")
            if then_text
            else ""
        )

    elif "then" in conditional_content and "properties" in conditional_content["then"]:
        then_not_text = ""
        then_text = get_if_condition_text(
            conditional_content["then"],
            md_file,
            export_folder,
            breadcrums=copy.deepcopy(breadcrums),
        )
    elif "then" in conditional_content:
        then_not_text = (
            get_then_not_text(conditional_content["then"]["not"], md_file)
            if "not" in conditional_content["then"]
            else ""
        )
        reqs = conditional_content["then"].get("required", [])
        then_text = (
            ", ".join([f"{get_inline_link(el, md_file)}" for el in reqs])
            + (" is present" if len(reqs) == 1 else " are present")
            if reqs
            else ""
        )

    if "then" in conditional_content:
        if then_not_text or then_text:
            conditional_records.append(
                [if_text, "<br> AND <br>".join(filter(bool, [then_text, then_not_text]))]
            )
    if "else" in conditional_content and "properties" in conditional_content["else"]:
        elseif_text = get_if_condition_text(
            conditional_content["if"],
            md_file,
            export_folder,
            not_=True,
            breadcrums=copy.deepcopy(breadcrums),
        )
        else_text = get_if_condition_text(
            conditional_content["else"],
            md_file,
            export_folder,
            breadcrums=copy.deepcopy(breadcrums),
        )
        if prev_if_text:
            elseif_text = f"{prev_if_text} AND {elseif_text}"
        conditional_records.append([elseif_text, else_text])
    elif "else" in conditional_content:
        elseif_text = get_if_condition_text(
            conditional_content["if"],
            md_file,
            export_folder,
            not_=True,
            breadcrums=copy.deepcopy(breadcrums),
        )
        if prev_if_text:
            elseif_text = f"{prev_if_text} AND {elseif_text}"
        if "if" in conditional_content["else"]:
            conditional_records.extend(
                get_conditional_table_record(
                    conditional_content["else"],
                    md_file,
                    export_folder,
                    prev_if_text=elseif_text,
                    breadcrums=copy.deepcopy(breadcrums),
                )
            )
        should_not_text = ""
        if "not" in conditional_content["else"]:
            should_not_text = (
                get_then_not_text(conditional_content["else"]["not"], md_file)
                if "not" in conditional_content["else"]
                else ""
            )
        reqs = conditional_content.get("else", {}).get("required", [])
        should_text = (
            ", ".join([f"{get_inline_link(el, md_file)}" for el in reqs])
            + (" are present" if len(reqs) > 1 else " is present")
            if reqs
            else ""
        )
        if should_not_text or should_text:
            conditional_records.append(
                [elseif_text, "<br> AND <br>".join(filter(bool, [should_text, should_not_text]))]
            )
    if "not" in conditional_content:
        if "allOf" in conditional_content["not"]:
            allof_with_props = [item for item in conditional_content["not"]["allOf"]]
            all_of_texts = []
            for all_of in allof_with_props:
                all_of_texts.append(
                    get_if_condition_text(
                        all_of, md_file, export_folder, breadcrums=copy.deepcopy(breadcrums)
                    )
                )
            if all_of_texts:
                conditional_records.append(
                    [if_text, " AND ".join(all_of_texts) + " <br> IS NOT TRUE."]
                )

    return conditional_records


def handle_conditional_allofs(
    allof_contents: list[dict], md_file: MdUtils, export_folder: Path, breadcrums: list = []
):
    md_file.new_line()
    md_file.new_header(level=3, title="Conditional Validation", add_table_of_contents="n")
    list_of_strings = [
        "`if true`",
        "`validate`",
    ]
    num_rows = 1
    for item in allof_contents:
        records = get_conditional_table_record(
            item, md_file, export_folder, breadcrums=copy.deepcopy(breadcrums)
        )
        for record in records:
            list_of_strings.extend(record)
            num_rows += 1

    md_file.new_line()
    md_file.new_table(columns=2, rows=num_rows, text=list_of_strings, text_align="center")


def handle_allofs(
    allofs: list[dict], md_file: MdUtils, export_folder: Path, breadcrums: list = []
):
    md_file.new_line()
    md_file.new_header(level=2, title="allOf Requirement", add_table_of_contents="n")
    conditional_allofs = [allof for allof in allofs if check_if_conditional_validation(allof)]
    if conditional_allofs:
        handle_conditional_allofs(
            conditional_allofs, md_file, export_folder, breadcrums=copy.deepcopy(breadcrums)
        )


def generate_markdown_for_object(contents: dict, export_folder: Path, breadcrums: list = []):
    """Function to generate markdown file for object recursively."""

    if "properties" in contents and "type" not in contents:
        contents["type"] = "object"

    if "title" in contents and "type" not in contents:
        contents["type"] = "object"

    md_file = get_md_file_from_title(contents.get("title"), export_folder)
    if breadcrums:
        md_file.new_line(" / ".join(breadcrums))

    breadcrums.append(get_hyperlinked_object_text(contents.get("title"), md_file))
    md_file.new_header(level=1, title=contents.get("title"))
    if "$id" in contents:
        add_link_to_json_schema(md_file, contents.get("$id"))

    if contents.get("type") == "array":
        items = contents.get("items")
        type_text = (
            get_hyperlinked_object_text(items.get("title"), md_file)
            if "enum" not in items
            else "string"
        )
        md_file.new_line(f"Type: array[{type_text}]")
        if items.get("type") == "object":
            generate_markdown_for_object(items, export_folder, copy.deepcopy(breadcrums))

        if "enum" in items:
            handle_enums(items["enum"], md_file)

        if "anyOf" in items:
            handle_anyofs(items["anyOf"], md_file, export_folder, copy.deepcopy(breadcrums))

        md_file.create_md_file()

    elif contents.get("type") == "object":
        md_file.new_line("Type: `object`")
        md_file.new_line(
            f"Additional Properties Allowed: `{contents.get('additionalProperties', True)}`"
        )
        if "properties" in contents:
            add_table_of_properties(contents, md_file)
            for _, ppty_dict in contents["properties"].items():
                if ppty_dict.get("type") in ["object", "array"] or "properties" in ppty_dict:
                    generate_markdown_for_object(
                        ppty_dict, export_folder, copy.deepcopy(breadcrums)
                    )

        if "oneOf" in contents:
            handle_oneofs(contents.get("oneOf"), md_file, export_folder, copy.deepcopy(breadcrums))

        if "allOf" in contents:
            handle_allofs(
                contents.get("allOf"), md_file, export_folder, breadcrums=copy.deepcopy(breadcrums)
            )

        if "if" in contents:
            handle_allofs([contents], md_file, export_folder, copy.deepcopy(breadcrums))

        if "anyOf" in contents:
            handle_anyofs(contents.get("anyOf"), md_file, export_folder, copy.deepcopy(breadcrums))

        if "properties" in contents:
            add_ppty_details(contents, md_file)

        md_file.create_md_file()
    else:
        raise Exception(f"Unknown type: {contents}")


def resolve_refs(schema, defs=None):
    """Recursively resolve $ref in a JSON Schema without using RefResolver."""
    if defs is None:
        defs = schema.get("$defs", {})  # Extract definitions from the root schema

    if isinstance(schema, dict):
        if "$ref" in schema:
            ref_key = schema["$ref"].split("/")[-1]  # Extract ref key from "#/$defs/mydef"
            if ref_key in defs:
                return resolve_refs(defs[ref_key], defs)  # Recursively resolve ref
            else:
                raise ValueError(f"Reference '{ref_key}' not found in $defs")
        return {k: resolve_refs(v, defs) for k, v in schema.items()}

    elif isinstance(schema, list):
        return [resolve_refs(item, defs) for item in schema]

    return schema


def generate_markdown_files(json_schema_file: Path, export_folder: Path):
    """Function for generating markdown files associated with json schema file."""

    contents = read_json_file(json_schema_file)
    resolved_contents = resolve_refs(contents)
    generate_markdown_for_object(resolved_contents, export_folder, copy.deepcopy([]))


def get_folder_name_from_file_path(file_path: Path) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", get_file_name_from_file_path(file_path)).lower()


def get_title_from_file_path(file_path: Path) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", " ", get_file_name_from_file_path(file_path)).title()


def get_file_name_from_file_path(file_path: Path) -> str:
    return file_path.name.split(".")[0]


def get_navs_as_dict(schema_folder: Path) -> list[dict[str, str]]:
    nav_items = []
    for file in schema_folder.iterdir():
        title = get_title_from_file_path(file)
        folder_name = get_folder_name_from_file_path(file)
        nav_items.append({title: f"{folder_name}/{folder_name}.md"})
    return nav_items


def generate_markdown_files_from_folder(
    schema_folder: Path, export_path: Path, preamble: Path = None, title: str = None
):
    """Function for generating markdown files from multiple schema files in a folder."""
    index_md = MdUtils(file_name=str(export_path / "index.md"))
    if title:
        index_md.new_header(level=1, title=title)
    if preamble:
        with open(preamble, "r", encoding="utf-8") as file_pointer:
            preamble_contents = file_pointer.read()
        index_md.write(preamble_contents)
        index_md.new_line()

    link_items = []
    for file in schema_folder.iterdir():
        if file.suffix != ".json":
            continue
        folder_name = get_folder_name_from_file_path(file)
        title = get_title_from_file_path(file)
        out_folder = export_path / folder_name
        out_folder.mkdir(exist_ok=True)
        generate_markdown_files(file, out_folder)
        link_items.append(
            index_md.new_inline_link(link=f"{folder_name}/{folder_name}.md", text=title)
        )
    link_items.sort()
    index_md.new_list(link_items)
    index_md.create_md_file()


if __name__ == "__main__":
    schema_file = Path(__file__).parent / "../src/gridmeta/schemas"
    export_path = Path("docs/schemas")
    export_path.mkdir(exist_ok=True)
    generate_markdown_files_from_folder(schema_file, export_path)
