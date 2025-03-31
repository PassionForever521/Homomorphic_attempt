import xml.etree.ElementTree as ET

def parse_config(file_path):
    global safety_para, sigma, theta, k
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        safety_para = root.find("safety_para").text.strip().lower() == "true"
        sigma = float(root.find("sigma").text.strip())
        theta = float(root.find("delta").text.strip())
        k = int(root.find("k").text.strip())
        print(f"[CONFIG] sigma={sigma}, theta={theta}, k={k}, safety={safety_para}")
    except Exception as e:
        print(f"Error reading configuration: {e}")
