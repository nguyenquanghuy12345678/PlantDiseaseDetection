"""
Treatment recommendations for plant diseases
Vietnamese agricultural context
"""

# Disease treatment database
TREATMENT_DATABASE = {
    "Lá khỏe mạnh": {
        "diagnosis": "Lá cây khỏe mạnh, không có dấu hiệu bệnh",
        "treatment": "Tiếp tục chăm sóc bình thường và theo dõi",
        "prevention": [
            "Duy trì tưới nước đều đặn",
            "Bón phân cân đối NPK",
            "Loại bỏ cỏ dại xung quanh"
        ],
        "severity": "none"
    },
    
    "Bệnh đốm lá": {
        "diagnosis": "Bệnh do nấm gây ra, xuất hiện các đốm tròn trên lá",
        "treatment": "Sử dụng thuốc trừ nấm Mancozeb 80WP hoặc Carbendazim",
        "prevention": [
            "Tỉa bớt lá bị bệnh và tiêu hủy",
            "Tránh tưới nước vào lá, chỉ tưới gốc",
            "Cải thiện thoát nước, không để úng",
            "Phun thuốc dự phòng 7-10 ngày/lần"
        ],
        "severity": "medium"
    },
    
    "Bệnh héo xanh": {
        "diagnosis": "Bệnh do vi khuẩn, cây héo nhanh dù đất còn ẩm",
        "treatment": "Sử dụng thuốc kháng sinh nông nghiệp (Streptomycin Sulfate)",
        "prevention": [
            "Nhổ bỏ và tiêu hủy cây bị bệnh",
            "Khử trùng đất bằng vôi bột",
            "Luân canh với các loại cây khác",
            "Không trồng lại cùng loại cây trong 2-3 năm"
        ],
        "severity": "high"
    },
    
    "Bệnh đạo ôn": {
        "diagnosis": "Bệnh nấm nguy hiểm, lây lan nhanh trong điều kiện ẩm",
        "treatment": "Phun thuốc Tricyclazole 75WP hoặc Isoprothiolane",
        "prevention": [
            "Tăng cường thông thoáng cho cây",
            "Bón phân Kali để tăng sức đề kháng",
            "Phun thuốc phòng bệnh khi thời tiết mưa ẩm",
            "Thu hoạch và tiêu hủy rơm rạ sau vụ"
        ],
        "severity": "high"
    },
    
    "Bệnh khô vằn": {
        "diagnosis": "Bệnh do nấm, lá có vằn vàng khô dần",
        "treatment": "Sử dụng Validamycin hoặc Propiconazole",
        "prevention": [
            "Cắt bỏ lá bị bệnh",
            "Phun thuốc đều đặn mỗi 10-14 ngày",
            "Bón phân hữu cơ tăng sức đề kháng",
            "Tránh bón đạm quá nhiều"
        ],
        "severity": "medium"
    },
    
    "Bệnh thán thư": {
        "diagnosis": "Bệnh nấm, tạo vết lõm trên thân và trái",
        "treatment": "Phun Copper Oxychloride hoặc Mancozeb",
        "prevention": [
            "Tỉa cành tạo thoáng",
            "Phun thuốc phòng bệnh trước mưa",
            "Thu gom và tiêu hủy phần cây bị bệnh",
            "Sử dụng giống kháng bệnh"
        ],
        "severity": "medium"
    },
    
    "Bệnh gỉ sắt": {
        "diagnosis": "Bệnh nấm gỉ sắt, xuất hiện đốm màu nâu đỏ",
        "treatment": "Sử dụng Tebuconazole hoặc Triadimefon",
        "prevention": [
            "Loại bỏ lá già và lá bị bệnh",
            "Tăng cường kali và photpho",
            "Phun thuốc 2-3 lần cách nhau 7-10 ngày",
            "Giữ khoảng cách trồng hợp lý"
        ],
        "severity": "low"
    },
    
    "Bệnh xoăn lá": {
        "diagnosis": "Do virus hoặc rệp gây ra, lá xoăn và biến dạng",
        "treatment": "Phun thuốc diệt rệp (Imidacloprid hoặc Acetamiprid)",
        "prevention": [
            "Nhổ bỏ cây bị bệnh nặng",
            "Diệt rệp truyền bệnh bằng bẫy vàng",
            "Sử dụng giống kháng virus",
            "Trồng cây bẫy xung quanh vườn"
        ],
        "severity": "high"
    },
    
    "Bệnh thối rễ": {
        "diagnosis": "Nấm tấn công rễ, cây vàng lá và chậm lớn",
        "treatment": "Tưới Metalaxyl hoặc Fosetyl-Al vào gốc",
        "prevention": [
            "Cải thiện hệ thống thoát nước",
            "Tránh tưới nước ngập úng",
            "Bón vôi để cân bằng pH đất",
            "Sử dụng giống ghép có gốc kháng bệnh"
        ],
        "severity": "high"
    },
    
    "Bệnh nấm phấn trắng": {
        "diagnosis": "Nấm phấn trắng phủ trên bề mặt lá",
        "treatment": "Phun Sulfur hoặc Myclobutanil",
        "prevention": [
            "Tăng độ thoáng, cắt tỉa cành",
            "Tránh tưới nước lên lá",
            "Phun dung dịch lưu huỳnh định kỳ",
            "Trồng cây giữa các hàng đủ khoảng cách"
        ],
        "severity": "low"
    },
    
    "Bệnh đốm vòng": {
        "diagnosis": "Xuất hiện vết đốm hình vòng tròn trên lá",
        "treatment": "Sử dụng thuốc Chlorothalonil hoặc Mancozeb",
        "prevention": [
            "Loại bỏ lá bệnh và tiêu hủy",
            "Không tưới nước lên tán lá",
            "Luân canh với cây họ khác",
            "Phun thuốc phòng bệnh định kỳ"
        ],
        "severity": "medium"
    },
    
    "Bệnh khảm lá": {
        "diagnosis": "Lá có vết khảm màu vàng xanh xen kẽ do virus",
        "treatment": "Không có thuốc đặc trị, phòng ngừa côn trùng truyền bệnh",
        "prevention": [
            "Nhổ bỏ cây bệnh ngay khi phát hiện",
            "Phun thuốc trừ rệp, bọ trĩ, ve sầu",
            "Sử dụng giống kháng virus",
            "Khử trùng dụng cụ canh tác",
            "Trồng cây rào chắn ngăn côn trùng"
        ],
        "severity": "high"
    },
    
    "Bệnh thối quả": {
        "diagnosis": "Quả bị thối, có mùi hôi, lan nhanh",
        "treatment": "Phun Copper hydroxide hoặc Mancozeb",
        "prevention": [
            "Thu hoạch đúng lúc, tránh chín quá",
            "Tránh làm thương quả khi thu hoạch",
            "Bảo quản nơi khô ráo, thoáng mát",
            "Phun thuốc phòng bệnh trước thu hoạch",
            "Loại bỏ quả bệnh ngay"
        ],
        "severity": "high"
    },
    
    "Bệnh héo rũ": {
        "diagnosis": "Cây héo rũ, lá vàng rụng, thân yếu",
        "treatment": "Tưới Metalaxyl hoặc Fosetyl-Al vào gốc cây",
        "prevention": [
            "Cải thiện thoát nước, tránh ngập úng",
            "Không trồng quá dày",
            "Bón phân cân đối, tránh bón đạm nhiều",
            "Sử dụng giống kháng bệnh",
            "Xử lý đất trước khi trồng"
        ],
        "severity": "high"
    },
    
    "Bệnh vàng lá": {
        "diagnosis": "Lá chuyển vàng, cây sinh trưởng kém",
        "treatment": "Bón phân đạm, phun phân lá chứa Nitrogen và vi lượng",
        "prevention": [
            "Bón phân cân đối NPK",
            "Kiểm tra và cải thiện pH đất",
            "Bổ sung vi lượng (Fe, Zn, Mg)",
            "Tưới nước đầy đủ, tránh úng",
            "Xử lý sâu bệnh hại rễ nếu có"
        ],
        "severity": "low"
    }
}


def get_treatment_info(disease_name):
    """
    Get treatment information for a disease
    
    Args:
        disease_name: Name of the disease
    
    Returns:
        dict: Treatment information or default message
    """
    # Look up disease in database
    treatment = TREATMENT_DATABASE.get(disease_name)
    
    if treatment:
        return treatment
    else:
        # Default response for unknown diseases
        return {
            "diagnosis": "Không tìm thấy thông tin cụ thể cho bệnh này",
            "treatment": "Vui lòng tham khảo ý kiến chuyên gia nông nghiệp",
            "prevention": [
                "Giữ vệ sinh vườn cây sạch sẽ",
                "Theo dõi cây thường xuyên",
                "Tham khảo trạm khuyến nông địa phương"
            ],
            "severity": "unknown"
        }


def get_all_diseases():
    """Get list of all diseases in database"""
    return list(TREATMENT_DATABASE.keys())


def get_severity_level(disease_name):
    """Get severity level of a disease"""
    treatment = TREATMENT_DATABASE.get(disease_name)
    if treatment:
        return treatment.get('severity', 'unknown')
    return 'unknown'
