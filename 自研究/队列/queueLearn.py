import random
import queue,time

AirLineList = [
            "ICN-FUK", "ICN-HSG", "ICN-KIX", "ICN-KMJ", "ICN-NGO", "ICN-OIT", "ICN-OKA", "ICN-NRT",
            "ICN-RMQ", "ICN-SHE", "ICN-SYX", "ICN-TAO", "ICN-TNA", "ICN-MFM", "ICN-HKG", "ICN-KHH",
            "ICN-WNZ", "ICN-VTE", "ICN-CRK", "ICN-KLO", "ICN-BKK", "ICN-CNX", "ICN-CXR", "ICN-DAD",
            "ICN-HAN", "ICN-SGN", "ICN-GUM", "ICN-SPN", "GMP-CJU", "GMP-TSA", "CJU-GMP", "CJU-TAE",
            "CJU-KWJ", "CJU-MWX", "CJU-NGO", "CJU-NRT", "CJU-KIX", "CJU-TPE", "CJU-TSA", "CJU-HKG",
            "CJU-DYG", "CJU-YNJ", "CJU-CEB", "CJU-KLO", "CJU-BKK", "CJU-CXR", "CJU-DAD", "CJU-HAN",
            "CJU-GUM", "TAE-CJU", "TAE-OKA", "TAE-NRT", "TAE-KIX", "TAE-FUK", "TAE-TPE", "TAE-HKG",
            "TAE-DYG", "TAE-YNJ", "TAE-CEB", "TAE-KLO", "TAE-BKK", "TAE-CXR", "TAE-DAD", "TAE-HAN",
            "TAE-GUM", "PUS-KIX", "PUS-KHH", "PUS-RMQ", "PUS-TPE", "PUS-DAD", "PUS-HAN", "PUS-VTE",
            "MWX-CJU", "KWJ-CJU", "KWJ-KIX", "KWJ-NRT", "OKA-ICN", "OKA-TAE", "OKA-RMQ", "OKA-KHH",
            "OKA-BKK", "OKA-SGN", "OKA-KLO", "OKA-HAN", "OKA-DAD", "OKA-CXR", "OKA-CEB", "OKA-VTE",
            "OKA-GUM", "OKA-SPN", "OIT-ICN", "OIT-RMQ", "OIT-KHH", "OIT-SGN", "OIT-KLO", "OIT-BKK",
            "OIT-HAN", "OIT-DAD", "OIT-CXR", "OIT-CRK", "OIT-CEB", "OIT-VTE", "OIT-GUM", "OIT-SPN",
            "NRT-ICN", "NRT-CJU", "NRT-TAE", "NRT-KWJ", "NRT-RMQ", "NRT-KHH", "NRT-VTE", "NRT-CEB",
            "NRT-KLO", "NRT-BKK", "NRT-CXR", "NRT-DAD", "NRT-HAN", "NRT-SGN", "NRT-GUM", "NRT-SPN", "NGO-ICN",
            "NGO-CJU", "NGO-RMQ", "NGO-KHH", "NGO-SGN", "NGO-KLO", "NGO-BKK", "NGO-HAN", "NGO-DAD", "NGO-CXR",
            "NGO-VTE", "NGO-GUM", "NGO-SPN", "CTS-RMQ", "CTS-KHH", "CTS-BKK", "CTS-SGN", "CTS-KLO", "CTS-HAN",
            "CTS-DAD", "CTS-CXR", "CTS-CEB", "CTS-VTE", "CTS-GUM", "CTS-SPN", "FUK-ICN", "FUK-TAE", "FUK-RMQ",
            "FUK-KHH", "FUK-BKK", "FUK-SGN", "FUK-KLO", "FUK-HAN", "FUK-DAD", "FUK-CXR", "FUK-CRK", "FUK-VTE",
            "FUK-GUM", "FUK-SPN", "HSG-ICN", "HSG-RMQ", "HSG-KHH", "HSG-SGN", "HSG-KLO", "HSG-BKK", "HSG-HAN",
            "HSG-DAD", "HSG-CXR", "HSG-CRK", "HSG-CEB", "HSG-VTE", "HSG-GUM", "HSG-SPN", "KIX-ICN", "KIX-CJU",
            "KIX-TAE", "KIX-KWJ", "KIX-PUS", "KIX-RMQ", "KIX-KHH", "KIX-VTE", "KIX-CEB", "KIX-KLO", "KIX-BKK",
            "KIX-CXR", "KIX-DAD", "KIX-HAN", "KIX-SGN", "KIX-GUM", "KIX-SPN", "KMJ-ICN", "KMJ-RMQ", "KMJ-KHH",
            "KMJ-SGN", "KMJ-KLO", "KMJ-BKK", "KMJ-HAN", "KMJ-DAD", "KMJ-CXR", "KMJ-CRK", "KMJ-CEB", "KMJ-VTE",
            "KMJ-GUM", "KMJ-SPN", "KOJ-RMQ", "KOJ-KHH", "KOJ-BKK", "KOJ-SGN", "KOJ-KLO", "KOJ-HAN", "KOJ-DAD",
            "KOJ-CXR", "KOJ-CRK", "KOJ-CEB", "KOJ-VTE", "KOJ-GUM", "KOJ-SPN", "RMQ-ICN", "RMQ-PUS", "RMQ-CTS",
            "RMQ-OKA", "RMQ-OIT", "RMQ-NRT", "RMQ-NGO", "RMQ-KOJ", "RMQ-KMJ", "RMQ-KIX", "RMQ-HSG", "RMQ-FUK",
            "RMQ-GUM", "RMQ-SPN", "SHE-ICN", "YNJ-CJU", "YNJ-TAE", "WNZ-ICN", "WNZ-SPN", "TSA-GMP", "TSA-CJU",
            "TPE-CJU", "TPE-TAE", "TPE-PUS", "TNA-ICN", "TNA-CTS", "TNA-OKA", "TNA-OIT", "TNA-NRT", "TNA-NGO",
            "TNA-KOJ", "TNA-KMJ", "TNA-KIX", "TNA-HSG", "TNA-FUK", "TNA-SPN", "TAO-ICN", "SYX-ICN", "MFM-ICN",
            "DYG-CJU", "DYG-TAE", "HKG-ICN", "HKG-CJU", "HKG-TAE", "KHH-ICN", "KHH-PUS", "KHH-CTS", "KHH-OKA",
            "KHH-OIT", "KHH-NRT", "KHH-NGO", "KHH-KOJ", "KHH-KMJ", "KHH-KIX", "KHH-HSG", "KHH-FUK", "KHH-GUM",
            "KHH-SPN", "SGN-ICN", "SGN-CTS", "SGN-OIT", "SGN-NRT", "SGN-NGO", "SGN-KOJ", "SGN-KMJ", "SGN-KIX",
            "SGN-HSG", "SGN-FUK", "SGN-OKA", "VTE-ICN", "VTE-PUS", "CNX-ICN", "CRK-ICN", "CXR-ICN", "CXR-CJU",
            "CXR-TAE", "CXR-HSG", "CXR-OKA", "CXR-OIT", "CXR-NRT", "CXR-NGO", "CXR-KOJ", "CXR-CTS", "CXR-KIX",
            "CXR-FUK", "CXR-KMJ", "DAD-ICN", "DAD-CJU", "DAD-TAE", "DAD-PUS", "DAD-HSG", "DAD-OKA", "DAD-OIT",
            "DAD-NRT", "DAD-NGO", "DAD-CTS", "DAD-KMJ", "DAD-KIX", "DAD-FUK", "DAD-KOJ", "BKK-ICN", "BKK-CJU",
            "BKK-TAE", "BKK-HSG", "BKK-OKA", "BKK-OIT", "BKK-NRT", "BKK-NGO", "BKK-KOJ", "BKK-CTS", "BKK-KIX",
            "BKK-FUK", "BKK-KMJ", "HAN-ICN", "HAN-CJU", "HAN-TAE", "HAN-PUS", "HAN-HSG", "HAN-OKA", "HAN-OIT",
            "HAN-NRT", "HAN-NGO", "HAN-CTS", "HAN-KMJ", "HAN-KIX", "HAN-FUK", "HAN-KOJ", "KLO-ICN", "KLO-CJU",
            "KLO-TAE", "CEB-CJU", "CEB-TAE", "SPN-ICN", "GUM-ICN", "GUM-CJU", "GUM-TAE", "GUM-KIX", "GUM-NGO",
        ]

q = queue.Queue()
q.put("0")
q.put(1)
q.put(True)
q.put({"a":"bb"})
q.put(["1",2])
print(q.qsize())
print(type(q.get()))
print(type(q.get()))
print(type(q.get()))
print(type(q.get()))
print(type(q.get()))
print(type(q.get()))

print(q.qsize())
