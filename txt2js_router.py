import argparse

# 1. 解析命令行参数 -f xxx.txt
parser = argparse.ArgumentParser(description='txt路径 → 自动生成Vue路由跳转JS文件')
parser.add_argument('-f', '--file', required=True, help='指定存放路径的txt文件')
args = parser.parse_args()

try:
    # 2. 读取路径文本
    with open(args.file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 清洗路径（去空行、换行）
    path_list = []
    for line in lines:
        path = line.strip()
        if path:
            path_list.append(f'"{path}"')

    # 拼接数组字符串
    paths_str = ',\n  '.join(path_list)

    # 3. 完整的 JS 自动跳转代码（真正3秒一跳，不刷新）
    js_content = f'''// Vue 自动路由跳转脚本
// 生成时间：自动生成
let pages = [
  {paths_str}
];

let index = 0;
function navigateNext() {{
  if (index >= pages.length) {{
    console.log("✅ 所有路由遍历完成");
    return;
  }}
  const path = pages[index];
  console.log("⏩ 跳转：", path);

  try {{
    // Vue Router 无刷新跳转
    if (window.$router) {{
      window.$router.push(path);
    }} else if (document.querySelector('#app')?.__vue__?.$router) {{
      document.querySelector('#app').__vue__.$router.push(path);
    }} else {{
      window.location.href = path;
    }}

    index++;
    setTimeout(navigateNext, 3000);
  }} catch (err) {{
    console.error("❌ 跳转失败：", err);
  }}
}}

// 启动
navigateNext();
'''

    # 4. 保存到本地 JS 文件
    with open('auto_router.js', 'w', encoding='utf-8') as f:
        f.write(js_content)

    print('✅ 生成成功！')
    print('📄 输出文件：auto_router.js')
    print('🔗 使用方式：打开Vue项目 → F12控制台 → 粘贴整个文件运行')

except FileNotFoundError:
    print(f'❌ 错误：未找到文件 {args.file}')
except Exception as e:
    print(f'❌ 处理失败：{str(e)}')