"""Dịch tượng + ý nghĩa 64 quẻ (nguồn: lich.vutrungu.com) — dùng cho tooltip học Dịch."""

from .normalize import chuan_hoa

# key = tên quẻ (chuẩn hoá) -> {ten: tên đầy đủ + "X dã", chi_tuong, y_nghia}
DICH_TUONG = {
    'BÁC': {
        "ten": 'SƠN ĐỊA BÁC: Lạc dã - TIÊU ĐIỀU',
        "chi_tuong": 'Lục thân băng thán chi tượng: Tượng bà con thân thích xa lìa nhau.',
        "y_nghia": 'Đẽo gọt, lột cướp đi, không có lợi, rụng rớt, đến rồi lại đi, tản lạc, lạt lẽo nhau, xa lìa nhau, hoang vắng, buồn thảm.',
    },
    'BÍ': {
        "ten": 'SƠN HỎA BÍ: Sức dã - QUANG MINH',
        "chi_tuong": 'Quang minh thông đạt chi tượng: Tượng quang minh, sáng sủa, thấu suốt.',
        "y_nghia": 'Trang sức, sửa sang, trang điểm, thấu suốt, rõ ràng.',
    },
    'BĨ': {
        "ten": 'THIÊN ĐỊA BĨ: Tắc dã - GIÁN CÁCH',
        "chi_tuong": 'Thượng hạ tiếm loạn chi tượng: Tượng trên dưới lôi thôi.',
        "y_nghia": 'Bế tắc, không thông, không tương cảm nhau, xui xẻo, dèm pha, chê bai lẫn nhau, mạnh ai nấy theo ý riêng.',
    },
    'CÁCH': {
        "ten": 'TRẠCH HỎA CÁCH: Cải dã - CẢI BIẾN',
        "chi_tuong": 'Thiên uyên huyền cách chi tượng: Tượng vực trời xa thẳm.',
        "y_nghia": 'Bỏ lối cũ, cải cách, hoán cải, cách tuyệt, cánh chim thay lông.',
    },
    'CẤU': {
        "ten": 'THIÊN PHONG CẤU: Ngộ dã - TƯƠNG NGỘ',
        "chi_tuong": 'Phong vân bất trắc chi tượng: Tượng gặp gỡ thình lình, ít khi.',
        "y_nghia": 'Gặp gỡ, cấu kết, liên kết, kết hợp, móc nối, mềm gặp cứng.',
    },
    'CỔ': {
        "ten": 'SƠN PHONG CỔ: Sự dã - SỰ BIẾN',
        "chi_tuong": 'Âm hại tương liên chi tượng: Tượng điều hại cùng có liên hệ.',
        "y_nghia": 'Có sự không yên trong lòng, làm ngờ vực, khua, đánh, mua chuốc cái hại, đánh trống, làm cho sợ sệt, sửa lại cái lỗi trước đã làm.',
    },
    'DI': {
        "ten": 'SƠN LÔI DI: Dưỡng dã - DUNG DƯỠNG',
        "chi_tuong": 'Phi long nhập uyên chi tượng: Tượng rồng vào vực nghỉ ngơi.',
        "y_nghia": 'Chăm lo, tu bổ, càng thêm, ăn uống, bổ dưỡng, bồi dưỡng, ví như trời nuôi muôn vật, thánh nhân nuôi người.',
    },
    'DỰ': {
        "ten": 'LÔI ĐỊA DỰ: Duyệt dã - THUẬN ĐỘNG',
        "chi_tuong": 'Thượng hạ duyệt dịch chi tượng : Tượng trên dưới vui vẻ.',
        "y_nghia": 'Dự bị, dự phòng, canh chừng, sớm, vui vầy.',
    },
    'GIA NHÂN': {
        "ten": 'PHONG HỎA GIA NHÂN: Đồng dã - NẨY NỞ',
        "chi_tuong": 'Khai hoa kết tử chi tượng: Tượng trổ bông sinh trái, nẩy mầm.',
        "y_nghia": 'Người nhà, gia đinh, cùng gia đình, đồng chủng, đồng nghiệp, cùng xóm, sinh sôi, khai thác mở mang thêm.',
    },
    'GIẢI': {
        "ten": 'LÔI THỦY GIẢI: Tán dã - NƠI NƠI',
        "chi_tuong": 'Lôi vũ tác giải chi tượng: Tượng sấm động mưa bay.',
        "y_nghia": 'Làm cho tan đi, như làm tan sự nguy hiểm, giải phóng, giải tán, loan truyền, tuyên truyền, phân phát, lưu thông, ban rải, ân xá.',
    },
    'HOÁN': {
        "ten": 'PHONG THỦY HOÁN: Tán dã - LY TÁN',
        "chi_tuong": 'Thủy ngộ phong tắc hoán tán chi tượng: Tượng nước gặp gió thì phải tan, phải chạy.',
        "y_nghia": 'Lan ra tràn lan, tán thất, trốn đi xa, lánh xa, thất nhân tâm, hao hớt.',
    },
    'HÀM': {
        "ten": 'TRẠCH SƠN HÀM: Cảm dã - THỤ CẢM',
        "chi_tuong": 'Nam nữ giao cảm chi tượng: Tượng nam nữ có tình ý.',
        "y_nghia": 'Cảm xúc, thọ nhận, cảm ứng, nghĩ đến, nghe thấy, xúc động.',
    },
    'HẰNG': {
        "ten": 'LÔI PHONG HẰNG: Cửu dã - TRƯỜNG CỬU',
        "chi_tuong": 'Trường cửu chi nghĩa chi tượng: Tượng lâu bền như đạo nghĩa.',
        "y_nghia": 'Lâu dài, chậm chạp, đạo lâu bền như vợ chồng, kéo dài câu chuyện, thâm giao, nghĩa cố tri, xưa, cũ.',
    },
    'KHIÊM': {
        "ten": 'ĐỊA SƠN KHIÊM: Thoái dã - CÁO THOÁI',
        "chi_tuong": 'Thượng hạ mông lung chi tượng : Tượng trên dưới hoang mang.',
        "y_nghia": 'Khiêm tốn, nhún nhường, khiêm từ, cáo thoái, từ giã, lui vào trong, giữ gìn, nhốt vào trong, bế cửa.',
    },
    'KHUỂ': {
        "ten": 'HỎA TRẠCH KHUỂ: Quai dã - HỖ TRỢ',
        "chi_tuong": 'Hồ giả hổ oai chi tượng: Tượng con hồ nhờ oai con hổ.',
        "y_nghia": 'Trái lìa, lìa xa, hai bên lợi dụng lẫn nhau, cơ biến quai xảo, như cung tên.',
    },
    'KHỐN': {
        "ten": 'TRẠCH THỦY KHỐN: Nguy dã - NGUY LO',
        "chi_tuong": 'Thủ kỷ đãi thời chi tượng: Tượng giữ mình đợi thời.',
        "y_nghia": 'Cùng quẫn, bị người làm ách, lo lắng, cùng khổ, mệt mỏi, nguy cấp, lo hiểm nạn.',
    },
    'KIỂN': {
        "ten": 'THỦY SƠN KIỂN: Nạn dã - TRỞ NGẠI',
        "chi_tuong": 'Bất năng tiến giả chi tượng: Tượng không năng đi.',
        "y_nghia": 'Cản ngăn, chận lại, chậm chạp, què, khó khăn.',
    },
    'KÝ TẾ': {
        "ten": 'THỦY HỎA KÝ TẾ: Hợp dã - HIỆN HỢP',
        "chi_tuong": 'Hanh tiểu giả chi tượng: Tượng việc nhỏ thì thành.',
        "y_nghia": 'Gặp nhau, cùng nhau, đã xong, việc xong, hiện thực, ích lợi nhỏ.',
    },
    'LÂM': {
        "ten": 'ĐỊA TRẠCH LÂM: Đại dã - BAO QUẢN',
        "chi_tuong": 'Quân tử dĩ giáo tư chi tượng: Tượng người quân tử dạy dân, che chở, bảo bọc dân vô bờ bến.',
        "y_nghia": 'Việc lớn, người lớn, cha nuôi, vú nuôi, giáo học, nhà sư, kẻ cả, dạy dân, nhà thầu.',
    },
    'LÝ': {
        "ten": 'THIÊN TRẠCH LÝ: Lễ dã - LỘ HÀNH',
        "chi_tuong": 'Hổ lang đang đạo chi tượng: Tượng hổ lang đón đường.',
        "y_nghia": 'Nghi lễ, có chừng mực, khuôn phép, dẫm lên, không cho đi sai, có ý chận đường sái quá, hệ thống, pháp lý.',
    },
    'LỮ': {
        "ten": 'HỎA SƠN LỮ: Khách dã - THỨ YẾU',
        "chi_tuong": 'Ỷ nhân tác giá chi tượng: Tượng nhờ người mai mối.',
        "y_nghia": 'Đỗ nhờ, khách, ở đậu, tạm trú, kê vào, gá vào, ký ngụ bên ngoài, tính cách lang thang, ít người thân, không chính...',
    },
    'MINH SẢNG': {
        "ten": 'ĐỊA HỎA MINH SẢNG: Thương dã - HẠI ĐAU',
        "chi_tuong": 'Kinh cức mãn đồ chi tượng: Tượng gai góc đầy đường.',
        "y_nghia": 'Thương tích, bịnh hoạn, buồn lo, đau lòng, ánh sáng bị thương.',
    },
    'MÔNG': {
        "ten": 'SƠN THỦY MÔNG: Muội dã - BẤT MINH',
        "chi_tuong": 'Thiên võng tứ trương chi tượng: Tượng lưới trời giăng bốn mặt.',
        "y_nghia": 'Tối tăm, mờ ám, không minh bạch, che lấp, bao trùm, phủ chụp, ngu dại, ngờ nghệch.',
    },
    'NHU': {
        "ten": 'THỦY THIÊN NHU: Thuận dã - TƯƠNG HỘI',
        "chi_tuong": 'Quân tử hoan hội chi tượng: Tượng quân tử vui vẻ hội họp, ăn uống chờ thời.',
        "y_nghia": 'Chờ đợi vì hiểm đằng trườc, thuận theo, quây quần, hội tụ, vui hội, cứu xét, chầu về.',
    },
    'PHONG': {
        "ten": 'LÔI HỎA PHONG: Thịnh dã - HÒA MỸ',
        "chi_tuong": 'Chí đồng đạo hợp chi tượng: Tượng cùng đồng tâm hiệp lực.',
        "y_nghia": 'Thịnh đại, được mùa, nhiều người góp sức.',
    },
    'PHỆ HẠP': {
        "ten": 'HỎA LÔI PHỆ HẠP: Khiết dã - CẮN HỢP',
        "chi_tuong": 'Ủy mị bất chấn chi tượng: Tượng yếu đuối không chạy được.',
        "y_nghia": 'Cấu Hợp, bấu vấu, bấu quào, dày xéo, đay nghiến, phỏng vấn, hỏi han (học hỏi).',
    },
    'PHỤC': {
        "ten": 'ĐỊA LÔI PHỤC: Phản dã - TÁI HỒI',
        "chi_tuong": 'Sơn ngoại thanh sơn chi tượng: Tượng ngoài núi lại còn có núi',
        "y_nghia": 'Lại có, trở về, bên ngoài, phản phục.',
    },
    'QUAN': {
        "ten": 'PHONG ĐỊA QUAN: Quan dã - QUAN SÁT',
        "chi_tuong": 'Vân bình tụ tán chi tượng: Tượng bèo mây tan hợp.',
        "y_nghia": 'Xem xét, trông coi, cảnh tượng xem thấy, thanh tra, lướt qua, sơ qua, sơn phết, quét nhà.',
    },
    'QUY MUỘI': {
        "ten": 'LÔI TRẠCH QUY MUỘI: Tai dã - XÔN XAO',
        "chi_tuong": 'Ác quỷ vi sủng chi tượng: Tượng ma quái làm rối.',
        "y_nghia": 'Tai nạn, rối ren, lôi thôi, nữ chi chung, gái lấy chồng.',
    },
    'QUẢI': {
        "ten": 'TRẠCH THIÊN QUẢI: Quyết dã - DỨT KHOÁT',
        "chi_tuong": 'Ích chi cực tắc quyết chi tượng: Tượng lợi đã cùng ắt thôi.',
        "y_nghia": 'Dứt hết, biên cương, ranh giới, thành phần, thành khoảnh, quyết định, quyết nghị, cổ phần, thôi, khai lề lối.',
    },
    'SƯ': {
        "ten": 'ĐỊA THỦY SƯ: Chúng dã - CHÚNG TRỢ',
        "chi_tuong": 'Sĩ chúng ủng tòng chi tượng: Tượng chúng ủng hộ nhau.',
        "y_nghia": 'Đông chúng, vừa làm thầy, vừa làm bạn, học hỏi lẫn nhau, níu nắm nhau qua truông, nâng đỡ.',
    },
    'THUẦN CHẤN': {
        "ten": 'THUẦN CHẤN: Động dã - ĐỘNG DỤNG',
        "chi_tuong": 'Trùng trùng chấn kinh chi tượng : Tượng khắp cùng dấy động.',
        "y_nghia": 'Rung động, sợ hãi do chấn động, phấn phát, nổ vang, chấn khởi, chấn kinh.',
    },
    'THUẦN CẤN': {
        "ten": 'THUẦN CẤN: Chỉ dã - NGƯNG NGHỈ',
        "chi_tuong": 'Thủ cựu đãi thời chi tượng: Tượng giữ mức cũ đợi thời.',
        "y_nghia": 'Ngăn giữ, ở, thôi, dừng lại, đậy lại, gói ghém, ngăn cấm, vừa đúng chỗ.',
    },
    'THUẦN KHÔN': {
        "ten": 'THUẦN KHÔN: Thuận dã - NHU THUẬN',
        "chi_tuong": 'Nhu Hanh Lợi Trinh chi tượng: Tượng vạn vật có khởi đầu, lớn lên, toại chí, hóa thành.',
        "y_nghia": 'Thuận tòng, mềm dẻo, theo đường mà được lợi, hòa theo lẽ, chịu lấy.',
    },
    'THUẦN KHẢM': {
        "ten": 'THUẦN KHẢM: Hãm dã - HÃM HIỂM',
        "chi_tuong": 'Khổ tận cam lai chi tượng: Tượng hết khổ mới đến sướng.',
        "y_nghia": 'Hãm vào ở trong, xuyên sâu vào trong, đóng cửa lại, gập ghềnh, trắc trở, bắt buộc, kềm hãm, thắng.',
    },
    'THUẦN KIỀN': {
        "ten": 'THUẦN KIỀN: Kiện dã - CHÍNH YẾU',
        "chi_tuong": 'Nguyên Hanh Lợi Trinh chi tượng: Tượng vạn vật có khởi đầu, lớn lên, toại chí, hóa thành.',
        "y_nghia": 'Cứng mạnh, khô, lớn, khỏe mạnh, đức không nghỉ. Nguyên Hanh Lợi Trinh.',
    },
    'THUẦN LY': {
        "ten": 'THUẦN LY: Lệ dã - SÁNG CHÓI',
        "chi_tuong": 'Môn hộ bất ninh chi tượng: Tượng nhà cửa không yên.',
        "y_nghia": 'Sáng sủa, trống trải, trống trơn, tỏa ra, bám vào, phụ bám, phô trương ra ngoài.',
    },
    'THUẦN TỐN': {
        "ten": 'THUẦN TỐN: Thuận dã - THUẬN NHẬP',
        "chi_tuong": 'Âm dương thăng giáng chi tượng: Tượng khí âm dương lên xuống giao hợp.',
        "y_nghia": 'Theo lên theo xuống, theo tới theo lui, có sự dấu diếm ở trong.',
    },
    'THUẦN ĐOÀI': {
        "ten": 'THUẦN ĐOÀI: Duyệt dã - HIỆN ĐẸP',
        "chi_tuong": 'Hỉ dật mi tu chi tượng: Tượng vui hiện trên mặt, khẩu khí.',
        "y_nghia": 'Đẹp đẽ, ưa thích, vui hiện trên mặt, không buồn chán, cười nói, khuyết mẻ.',
    },
    'THÁI': {
        "ten": 'ĐỊA THIÊN THÁI: Thông dã - ĐIỀU HÒA',
        "chi_tuong": 'Thiên địa hòa xướng chi tượng: Tượng trời đất giao hòa.',
        "y_nghia": 'Thông hiểu, am tường, hiểu biết, thông suốt, quen biết, quen thuộc.',
    },
    'THĂNG': {
        "ten": 'ĐỊA PHONG THĂNG: Tiến dã - TIẾN THỦ',
        "chi_tuong": 'Phù giao trực thượng chi tượng: Tượng chòi đạp để ngoi lên trên.',
        "y_nghia": 'Thăng tiến, trực chỉ, tiến mau, bay lên, vọt tới trước, bay lên không trung, thăng chức, thăng hà.',
    },
    'TIẾT': {
        "ten": 'THỦY TRẠCH TIẾT: Chỉ dã - GIẢM CHẾ',
        "chi_tuong": 'Trạch thượng hữu thủy chi tượng: Tượng trên đầm có nước.',
        "y_nghia": 'Ngăn ngừa, tiết độ, kềm chế, giảm bớt, chừng mực, nhiều thì tràn.',
    },
    'TIỂU QUÁ': {
        "ten": 'LÔI SƠN TIỂU QUÁ: Quá dã - BẤT TÚC',
        "chi_tuong": 'Thượng hạ truân chuyên chi tượng: Tượng trên dưới gian nan, vất vả, buồn thảm.',
        "y_nghia": 'Thiểu lý, thiểu não, hèn mọn, nhỏ nhặt, bẩn thỉu, thiếu cường lực.',
    },
    'TIỂU SÚC': {
        "ten": 'PHONG THIÊN TIỂU SÚC: Tắc dã - DỊ ĐỒNG',
        "chi_tuong": 'Cầm sắt bất điệu chi tượng: Tượng tiếng đờn không hòa điệu.',
        "y_nghia": 'Lúc bế tắc, không đồng ý nhau, cô quả, súc oán, chứa mội oán giận, có ý trái lại, không hòa hợp, nhỏ nhen.',
    },
    'TIỆM': {
        "ten": 'PHONG SƠN TIỆM: Tiến dã - TUẦN TỰ',
        "chi_tuong": 'Phúc lộc đồng lâm chi tượng: Tượng phúc lộc cùng đến.',
        "y_nghia": 'Từ từ, thong thả đến, lần lần, bò tới, chậm chạp, nhai nhỏ nuốt vào.',
    },
    'TRUNG PHU': {
        "ten": 'PHONG TRẠCH TRUNG PHU: Tín dã - TRUNG THẬT',
        "chi_tuong": 'Nhu tại nội nhi đắc trung chi tượng: Tượng âm ở bên trong mà được giữa.',
        "y_nghia": 'Tín thật, không ngờ vực, có uy tín cho người tin tưởng, tín ngưỡng, ở trong.',
    },
    'TRUÂN': {
        "ten": 'THỦY LÔI TRUÂN: Nạn dã - GIAN LAO',
        "chi_tuong": 'Tiền hung hậu kiết chi tượng: Tượng trước dữ sau lành.',
        "y_nghia": 'Yếu đuối, chưa đủ sức, ngần ngại, do dự, vất vả, phải nhờ sự giúp đỡ.',
    },
    'TÙY': {
        "ten": 'TRẠCH LÔI TÙY: Thuận dã - DI ĐỘNG',
        "chi_tuong": 'Phản phúc bất định chi tượng: Tượng loại không ở.',
        "y_nghia": 'Cùng theo, mặc lòng, không có chí hướng, chỉ chìu theo, đại thể chủ việc di động, thuyên chuyển như chiếc xe.',
    },
    'TẤN': {
        "ten": 'HỎA ĐỊA TẤN: Tiến dã - HIỂN HIỆN',
        "chi_tuong": 'Long kiến trình tường chi tượng : Tượng rồng hiện điềm lành.',
        "y_nghia": 'Đi hoặc tới, tiến tới gần, theo mực thường, lửa đã hiện trên đất, trưng bày.',
    },
    'TỈNH': {
        "ten": 'THỦY PHONG TỈNH: Tịnh dã - TRẦM LẶNG',
        "chi_tuong": 'Kiền Khôn sất phối chi tượng: Tượng Trời Đất phối hợp lại.',
        "y_nghia": 'Ở chỗ nào cứ ở yên chỗ đó, xuống sâu, vực thẳm có nước, dưới sâu, cái giếng.',
    },
    'TỔN': {
        "ten": 'SƠN TRẠCH TỔN: Thất dã - TỔN HẠI',
        "chi_tuong": 'Phòng nhân ám toán chi tượng: Tượng đề phòng sự ngầm hại, hao tổn.',
        "y_nghia": 'Hao mất, thua thiệt, bớt kém, bớt phần dưới cho phần trên là tổn hại.',
    },
    'TỤNG': {
        "ten": 'THIÊN THỦY TỤNG: Luận dã - BẤT HÒA',
        "chi_tuong": 'Đại tiểu bất hòa chi tượng: Tượng lớn nhỏ không hòa.',
        "y_nghia": 'Bàn cãi, kiện tụng, bàn tính, cãi vã, tranh luận, bàn luận.',
    },
    'TỤY': {
        "ten": 'TRẠCH ĐỊA TỤY: Tụ dã - TRƯNG TẬP',
        "chi_tuong": 'Long vân tế hội chi tượng: Tượng rồng mây giao hội.',
        "y_nghia": 'Nhóm họp, biểu tình, dồn đống, quầng tụ nhau lại, kéo đến, kéo thành bầy.',
    },
    'TỶ': {
        "ten": 'THỦY ĐỊA TỶ: Tư dã - CHỌN LỌC',
        "chi_tuong": 'Khứ xàm nhiệm hiền chi tượng: Tượng bỏ nịnh dụng trung.',
        "y_nghia": 'Thân liền, gạn lọc, mật thiết, tư hữu riêng, trưởng đoàn, trưởng toán, chọn lựa.',
    },
    'VÔ VỌNG': {
        "ten": 'THIÊN LÔI VÔ VỌNG: Thiên tai dã - XÂM LẤN',
        "chi_tuong": 'Cương tự ngoại lai chi tượng: Tượng kẻ mạnh từ ngoài đến.',
        "y_nghia": 'Tai vạ, lỗi bậy bạ, không lề lối, không quy củ, càn đại, chống đối, khứng chịu.',
    },
    'VỊ TẾ': {
        "ten": 'HỎA THỦY VỊ TẾ: Thất dã - THẤT CÁCH',
        "chi_tuong": 'Ưu trung vọng hỷ chi tượng : Tượng trong cái lo có cái mừng.',
        "y_nghia": 'Thất bác, mất, thất bại, dở dang, chưa xong, nửa chừng.',
    },
    'ÍCH': {
        "ten": 'PHONG LÔI ÍCH: Ích dã - TIẾN ÍCH',
        "chi_tuong": 'Hồng hộc xung tiêu chi tượng: Tượng chim hồng, chim hộc bay qua mây mù.',
        "y_nghia": 'Thêm được lợi, giúp dùm, tiếng dội xa, vượt lên, phóng mình tới.',
    },
    'ĐẠI HỮU': {
        "ten": 'HỎA THIÊN ĐẠI HỮU: Khoan dã - CẢ CÓ',
        "chi_tuong": 'Kim ngọc mãn đường chi tượng: Tượng vàng bạc đầy nhà.',
        "y_nghia": 'Thong dong, dung dưỡng nhiều, độ lượng rộng, có đức dầy, chiếu sáng lớn.',
    },
    'ĐẠI QUÁ': {
        "ten": 'TRẠCH PHONG ĐẠI QUÁ: Họa dã - CẢ QUÁ',
        "chi_tuong": 'Nộn thảo kinh sương chi tượng: Tượng cỏ non bị sương tuyết.',
        "y_nghia": 'Cả quá ắt tai họa, quá mực thường, quá nhiều, giàu cương nghị ở trong..',
    },
    'ĐẠI SÚC': {
        "ten": 'SƠN THIÊN ĐẠI SÚC: Tụ dã - TÍCH TỤ',
        "chi_tuong": 'Đồng loại hoan hội chi tượng: Tượng đồng loại hội họp vui vẻ, cục bộ.',
        "y_nghia": 'Chứa tụ, súc tích, lắng tụ một chỗ, dự trữ, đựng, để dành.',
    },
    'ĐẠI TRÁNG': {
        "ten": 'LÔI THIÊN ĐẠI TRÁNG: Chí dã - TỰ CƯỜNG',
        "chi_tuong": 'Phượng tập đăng sơn chi tượng : Tượng phượng đậu trên núi.',
        "y_nghia": 'Ý riêng, bụng nghĩ, hướng thượng, ý định, vượng sức, thịnh đại, trên cao, chót vót, lên trên, chí khí, có lập trường.',
    },
    'ĐỈNH': {
        "ten": 'HỎA PHONG ĐỈNH: Định dã - NUNG ĐÚC',
        "chi_tuong": 'Luyện dược thành đơn chi tượng: Tượng luyện thuốc thành linh đơn.',
        "y_nghia": 'Đứng được, cặm đứng, trồng, nung nấu, rèn luyện, vững chắc, ước hẹn.',
    },
    'ĐỒNG NHÂN': {
        "ten": 'THIÊN HỎA ĐỒNG NHÂN: Thân dã - THÂN THIỆN',
        "chi_tuong": 'Hiệp lực đồng tâm chi tượng: Tượng cùng người hiệp lực.',
        "y_nghia": 'Trên dưới cùng lòng, cùng người ưa thích, cùng một bọn người.',
    },
    'ĐỘN': {
        "ten": 'THIÊN SƠN ĐỘN: Thoái dã - ẨN TRÁ',
        "chi_tuong": 'Báo ẩn nam sơn chi tượng: Tượng con báo ẩn ở núi nam.',
        "y_nghia": 'Lui, ẩn khuất, tránh đời, lừa dối, trá hình, có ý trốn tránh, trốn cái mặt đưa thấy cái lưng.',
    },
}


def mo_ta(ten_que):
    """Trả về dict {ten, chi_tuong, y_nghia} của một quẻ, hoặc None."""
    return DICH_TUONG.get(chuan_hoa(ten_que))
