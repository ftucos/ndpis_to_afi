#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
import xml.etree.ElementTree as ET

def parse_ndpis(ndpis_path):
	"""
	Parse a .ndpis file and extract image paths and channel names.
	"""
	for raw_line in ndpis_path.read_text(encoding="utf-8", errors="replace").splitlines():
		line = raw_line.strip()
		m_file = re.match(r"^Image\d+=(.+\.ndpi)$", line, flags=re.IGNORECASE)

		if not m_file:
			continue

		image_name = m_file.group(1)
		image_path = str((ndpis_path.parent / image_name).resolve())

		# Extract channel from '-<channel>.ndpi' suffix.
		channel_name = re.match(r".+-([^-]+)\.ndpi$", image_name).group(1)

		yield {"Path": image_path, "ChannelName": channel_name}


def write_image_list_xml(images, out_xml):
	"""
	Write <ImageList><Image><Path>...</Path><ChannelName>...</ChannelName></Image>...</ImageList>
	"""
	root = ET.Element("ImageList")

	for rec in images:
		img_el = ET.SubElement(root, "Image")
		ET.SubElement(img_el, "Path").text = rec["Path"]
		ET.SubElement(img_el, "ChannelName").text = rec["ChannelName"]

	tree = ET.ElementTree(root)

	ET.indent(tree, space="  ", level=0)

	out_xml.parent.mkdir(parents=True, exist_ok=True)
	tree.write(out_xml, encoding="utf-8", xml_declaration=False)


def main():
	ap = argparse.ArgumentParser(description="Generate .afi files from .ndpis files.")
	ap.add_argument("source", type=Path, help="Source root folder to scan for .ndpis files.")
	args = ap.parse_args()

	source = args.source.resolve()

	for ndpis_path in source.rglob("*.ndpis"):
		images = parse_ndpis(ndpis_path)
		out_xml = ndpis_path.with_suffix(".afi")
		print(f"Writing {out_xml}...")
		write_image_list_xml(images, out_xml)

	print("Done.")

if __name__ == "__main__":
	main()
