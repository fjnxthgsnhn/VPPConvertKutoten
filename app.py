import flet as ft
import json
import os
import shutil

def main(page: ft.Page):
    page.title = "VOICEPEAK ポーズ調整ツール"
    # 初期ウィンドウサイズと位置
    page.window.width = 500
    page.window.height = 600
    page.window.center()
    page.scroll = "adaptive"
    page.theme_mode = "dark"

    DEFAULT_TOUTEN = 0.3  # 読点 (、)
    DEFAULT_KUTEN = 1.5   # 句点 (。)

    status_text = ft.Text("ファイルを選択してください", color="grey")
    
    touten_input = ft.TextField(
        label="読点 (、・) の長さ [秒]",
        value=str(DEFAULT_TOUTEN),
        keyboard_type="number",
        width=200
    )
    kuten_input = ft.TextField(
        label="句点 (。！？) の長さ [秒]",
        value=str(DEFAULT_KUTEN),
        keyboard_type="number",
        width=200
    )

    def process_vpp_file(file_path, touten_val, kuten_val):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw = f.read()
            try:
                data = json.loads(raw)
                trailing_notice = ""
            except json.JSONDecodeError as e:
                decoder = json.JSONDecoder()
                try:
                    data, idx = decoder.raw_decode(raw)
                    extra = raw[idx:].strip()
                    if extra:
                        # Ignore trailing garbage but note it to the user
                        trailing_notice = "（末尾の余分なデータを無視して読み込みました）"
                    else:
                        trailing_notice = "（末尾の空白を無視して読み込みました）"
                except Exception:
                    return False, f"エラー: JSONの読み込みに失敗しました ({e})"
            count = 0
            def walk_and_modify(node):
                nonlocal count
                if isinstance(node, dict):
                    if "s" in node and "syl" in node:
                        char = node["s"]
                        target_val = None
                        if char in {"、", "・"}:
                            target_val = touten_val
                        elif char in {"。", "！", "？"}:
                            target_val = kuten_val
                        if target_val is not None:
                            for syl in node.get("syl", []):
                                for p in syl.get("p", []):
                                    if p.get("s") == "pau":
                                        p["d"] = target_val
                                        count += 1
                    for key, value in node.items():
                        walk_and_modify(value)
                elif isinstance(node, list):
                    for item in node:
                        walk_and_modify(item)
            walk_and_modify(data)
            dir_name = os.path.dirname(file_path)
            base_name = os.path.basename(file_path)
            name, ext = os.path.splitext(base_name)
            new_path = os.path.join(dir_name, f"{name}_modified{ext}")
            with open(new_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=None, separators=(',', ':'))
            return True, f"????: {os.path.basename(new_path)} ({count}????){trailing_notice}"
        except Exception as e:
            return False, f"エラー: {str(e)}"

    def on_dialog_result(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        results = []
        try:
            t_val = float(touten_input.value)
            k_val = float(kuten_input.value)
        except ValueError:
            status_text.value = "エラー: 数値を正しく入力してください"
            status_text.color = "red"
            page.update()
            return
        for f in e.files:
            success, msg = process_vpp_file(f.path, t_val, k_val)
            icon = "check_circle" if success else "error"
            color = "green" if success else "red"
            results.append(ft.ListTile(
                leading=ft.Icon(icon, color=color),
                title=ft.Text(os.path.basename(f.path)),
                subtitle=ft.Text(msg)
            ))
        result_column.controls = results
        status_text.value = "処理が完了しました"
        status_text.color = "green"
        page.update()

    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.on_file_drop = lambda e: on_dialog_result(e)

    def pick_files_click(_):
        file_picker.pick_files(allow_multiple=True, allowed_extensions=["vpp"])

    result_column = ft.Column()

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("VOICEPEAK ポーズ一括変換", size=24, weight="bold"),
                ft.Divider(),
                ft.Text("設定", size=16, weight="bold"),
                ft.Row([touten_input, kuten_input]),
                ft.Divider(),
                ft.Text("ファイル操作", size=16, weight="bold"),
                ft.Text("以下ボタンからファイルを選択してください。（複数選択可）"),
                ft.ElevatedButton(
                    "ファイルを選択して実行",
                    icon="upload_file",
                    on_click=pick_files_click,
                    height=50
                ),
                ft.Divider(),
                status_text,
                result_column
            ]),
            padding=20
        )
    )

ft.app(target=main)
