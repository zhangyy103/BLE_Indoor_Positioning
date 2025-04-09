class DataParser:
    def __init__(self):
        # 更新数据格式定义
        self.data_format = {
            'header': '$POS',  # 匹配实际数据头
            'x_index': 1,       # x在分割后的索引
            'y_index': 2,       # y在分割后的索引
            'separator': ',',   # 分隔符
            'checksum_separator': '*'  # 校验和分隔符（如果启用）
        }

    def parse(self, raw_data):
        try:
            # 校验数据头
            if not raw_data.startswith(self.data_format['header']):
                return None, None

            # 分割数据（处理可能的校验和）
            main_part = raw_data.split(self.data_format['checksum_separator'])[0]
            parts = main_part.split(self.data_format['separator'])

            # 检查数据段数量
            if len(parts) < 3:
                return None, None

            # 提取坐标（直接转浮点数，无需除100）
            x = float(parts[self.data_format['x_index']])
            y = float(parts[self.data_format['y_index']])

            return x, y
        except (ValueError, IndexError) as e:
            print(f"解析错误: {e}")
            return None, None