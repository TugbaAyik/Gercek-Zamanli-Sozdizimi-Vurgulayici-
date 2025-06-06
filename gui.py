import tkinter as tk
from lexer_module import lexer
from main_parser import Parser

class CodeEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerçek Zamanlı Sözdizimi Denetleyici")

        self.text_area = tk.Text(root, wrap='word', undo=True, font=('Consolas', 12))
        self.text_area.pack(expand=True, fill='both')

        self.error_label = tk.Label(root, text="", fg="red", font=('Arial', 10, 'italic'))
        self.error_label.pack(anchor='w', padx=10, pady=2)

        self.text_area.bind("<KeyRelease>", self.on_text_change)

        #Tokenların renklerini tanımladım.

        self.token_colors = {
            'KEYWORD': 'blue',
            'IDENTIFIER': 'black',
            'NUMBER': 'orange',
            'STRING': 'green',
            'OPERATOR': 'purple',
            'DELIMITER': 'brown',
            'ERROR': 'red',
        }

    def on_text_change(self, event=None):
        code = self.text_area.get("1.0", tk.END)
        try:
            tokens = lexer(code)
            parser = Parser(tokens)
            parser.parse()
            self.error_label.config(text="✅ Sözdizimi doğru.", fg="green")
        except SyntaxError as e:
            tokens = lexer(code)  # Hata olsa da tokenları alıyoruz.
            self.error_label.config(text=str(e), fg="red")
        finally:
            self.highlight_tokens_no_pos(tokens)


    def clear_highlight(self):
        for tag in self.token_colors.keys():
            self.text_area.tag_remove(tag, "1.0", tk.END)
        self.text_area.tag_remove("error", "1.0", tk.END)

    def highlight_tokens_no_pos(self, tokens):
        self.clear_highlight()
        code = self.text_area.get("1.0", tk.END)
        lines = code.splitlines()

        # Her satırda tokenları sırayla arayıp renklendiriyoruz.
        line_index = 0
        for token_type, token_value in tokens:
            # Satır satır bulmaya çalışıyoruz.
            while line_index < len(lines):
                line = lines[line_index]
                idx = line.find(token_value)
                if idx != -1:
                    start_index = f"{line_index+1}.{idx}"
                    end_index = f"{line_index+1}.{idx + len(token_value)}"
                    color = self.token_colors.get(token_type, "black")
                    self.text_area.tag_add(token_type, start_index, end_index)
                    self.text_area.tag_config(token_type, foreground=color)
                    break
                else:
                    line_index += 1

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeEditorGUI(root)
    root.mainloop()
