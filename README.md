# 國立中正大學資訊管理／醫療資訊管理碩士論文 LaTeX 模板

唯一格式依據為本目錄的 **format.pdf**（2024/01/09 系務會議修正，18 頁）。
可選「資訊管理研究所」「醫療資訊管理研究所」，並可編譯碩士論文或碩士論文提案書。
本模板的題目、姓名、內容與文獻是明示的佔位資料；使用前請全部替換。

格式逐條判讀見 [docs/format-requirements.md](docs/format-requirements.md)，
實際編譯與 PDF 驗證結果見 [docs/validation.md](docs/validation.md)。
這是可編譯的排版模板，不是已完成簽章或獲系所核可的個人論文。

## 下載與建立自己的論文專案

GitHub 儲存庫：[TsengPinRuei/ccu-mis-thesis-latex-template](https://github.com/TsengPinRuei/ccu-mis-thesis-latex-template)。

- 想在 GitHub 保存自己的版本：點選 **Use this template → Create a new repository**，
  在自己的帳號建立論文專案。若會放入未公開研究或個人資料，可選 **Private**。
- 只想下載使用：點選 **Code → Download ZIP**，解壓縮後開啟專案資料夾。
- 已安裝 Git：使用以下指令下載，之後在該目錄編譯。

~~~sh
git clone https://github.com/TsengPinRuei/ccu-mis-thesis-latex-template.git
cd ccu-mis-thesis-latex-template
~~~

先依下方說明安裝 XeLaTeX、Biber 與合法授權字型，再修改 `thesis-config.tex`
及各章內容。儲存庫包含模板原始碼、格式依據與驗證文件；`output/`、暫存檔
及自備字型不納入版本控制，PDF 請在本機自行編譯產生。

## 快速開始

在此專案目錄使用：

~~~sh
bash scripts/build.sh           # 碩士論文，產生 output/pdf/main.pdf
bash scripts/build.sh proposal  # 提案，產生 output/pdf/proposal.pdf
bash scripts/build.sh spine     # 獨立書背，產生 output/pdf/spine.pdf
~~~

腳本採 XeLaTeX → Biber → XeLaTeX → XeLaTeX；書背不需 Biber。
每次更改內容或文獻後重跑；無需 latexmk，不使用 shell escape。
編譯失敗時先看 output/pdf/ 下對應的 .log／.blg；不要拿上一次留下的 PDF 當作新成果。
遇到缺字、溢出版心或未解決引用時腳本會回報失敗。

手動編譯論文的等效指令：

~~~sh
mkdir -p output/pdf
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=output/pdf main.tex
biber --input-directory output/pdf --output-directory output/pdf main
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=output/pdf main.tex
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=output/pdf main.tex
~~~

## 引擎、套件與字型

- 使用 **XeLaTeX**。已驗證 TeX Live 2025 與 Biber 2.21；其他環境需選相容的 biblatex/Biber 版本。
- 需要 fontspec、xeCJK、geometry、fix-cm、amsmath、amssymb、graphicx、xcolor、titlesec、
  tocloft、caption、zhnumber、pdfpages、eso-pic、hyperref、bookmark、etoolbox、
  indentfirst、biblatex、biblatex-apa。一般完整 TeX Live／MacTeX 可透過套件管理器補齊。
  若使用 BasicTeX，請依缺少的 .sty 名稱以 tlmgr 安裝相應套件。
- **中文必須有標楷體 DFKai-SB（嵌入 PDF 的名稱為 DFKaiShu-SB）**；
  **英文必須有 Times New Roman**（含 Bold、Italic）。
  標楷體與 Times New Roman 未隨專案散布，請使用合法授權的字型。
- 在 thesis-config.tex 的 ThesisCJKFont／ThesisLatinFont 設定正式字型名稱。
  也可將自己有權使用的 kaiu.ttf 放進 fonts/，並設定
  \ThesisCJKFontFile 為 fonts/kaiu.ttf。上傳 Overleaf 等環境亦須自行提供合法字型，
  選擇 XeLaTeX 及 Biber；不要將其他楷體改名冒充標楷體。
- 缺少規定字型會中止編譯，不會默默替換。標楷體沒有獨立粗體／斜體字檔，
  本模板明示使用 XeCJK 的 AutoFakeBold=2、AutoFakeSlant=.2，在同一標楷體上加粗或傾斜，
  以實作標題粗體、圖表題與註解斜體。英文粗斜體使用真正 Times New Roman 字檔。
- 數學符號採可縮放 Computer Modern；規範未指定數學符號字型，這是合理預設，
  不是將數學字型冒充 Times New Roman。正文中的中英文仍使用指定字型。

## 改基本資料

只修改 **thesis-config.tex**：

| 欄位 | 用途 |
| --- | --- |
| ThesisProgram | im：資訊管理研究所；him：醫療資訊管理研究所 |
| ThesisTitleZh / ThesisTitleEn | 中英文題目；共用中文題目保持純文字，由封面自動換行，修改後重看封面與書背 |
| ThesisAuthor | 填入姓名 |
| ThesisAdvisor / ThesisAdvisorTitle | 指導教授與稱謂，可依實際需要加入共同指導教授換行 |
| ThesisDegree | 預設碩士；來源未支持博士格式，改字樣不代表博士格式已驗證 |
| ThesisROCYear / ThesisMonth | 民國出版年、月份 |
| ThesisCohort | 書背畢業級別，未必等於出版年 |
| ThesisApprovalPDF | 正式已簽章 A4 審定書路徑；留空會放「非校方正式審定書」佔位頁 |
| ThesisSpineWidth / ThesisSpineFontSize | 裝訂店確認後的書背寬度、字級 |

proposal.tex 會以同一套設定輸出「碩士論文提案書」，並自動省略審定書、誌謝與兩種摘要。
不必手工刪頁。兩所共用來源同一版型，實際輸出只顯示選定的一個所名。

## 改正文、圖表與文獻

- main.tex：文件順序與章節載入入口。
- frontmatter/：誌謝與中英文摘要。
- chapters/01-introduction.tex、02-method.tex：章、節、小節、圖、表、公式與引用範例。
- chapters/appendices.tex：附錄 A、B，含 (A-1)、(A-2)、(B-1) 的自動編號。
- references.bib：文獻資料；用法與中文筆畫排序見 [docs/references.md](docs/references.md)。
- ccu-thesis.cls：底層版式，通常不需修改。
- ccu-bibliography.sty：APA 7 及中英排序，通常不需修改。

新增章使用 \chapter，節使用 \section，小節使用 \subsection，再在 main.tex 引入檔案。
章名與章數由研究需要決定，來源中的五章名稱只是示例。
每章及各組成項目另起新頁，沒有強制奇數頁開章；正文、文獻、附錄頁碼連續。
封底是一張無字、無浮水印、無頁碼的空白頁。

圖示範 \caption 在圖後，表示範 \caption 在表前。使用 \label、\ref 自動交叉引用。
\ccunote{...} 產生左對齊 10 點斜體註；\ccusource{\fullcite{鍵}.} 產生完整來源。
外部圖片請限制在 \linewidth 內；很長的圖題／表題要在修改後檢查目錄換行。

中文正文使用全形括號（包含 \ccucite 和 \ccueqref），表格括號半形，
英文段落用 \parencite／\textcite。公式本身的編號依規範保持半形括號，且置左。
中文文獻必須標 keywords={chinese} 並維護人工確認的 sortkey；
英文文獻不設 sortkey，由 Biber 按 `author` 欄位自動排序。文末 \ccureferences 放在正文之後、附錄之前。

## 規範差異及合理預設

來源的三處衝突採用以下設定：

1. 第 5 頁：依圖 5，校名粗體 36 點，其餘封面 24 點。
2. 第 1 頁對第 9–10 頁：依正式條文，封面 i，審定書 ii，前置頁連續編排。
3. 第 3 頁對第 1、17 頁：依版面範例，章後空兩行；節前兩行、節後一行。

採 A4 是依原檔實體大小；正文 12 點以 PDF/Word 的 bp（1/72 英寸）處理。
1.5 行高操作性設定為 **18 bp 基線距**，空白行也以 18 bp 計；
這不宣稱重建 Word 所有字型的自動行高算法。
頁碼距底 1 cm 以**文字基線**量測；字形可見下緣不是基線。
兩字段首縮排、章節 18/14/12 點、無字封底、數學符號字型、書背 15 mm 寬
都是依示例或未指定事項採用的明示預設。

使用 assets/CCU.jpg 作為校徽浮水印，保留原始淡藍色與白色背景。
模板直接載入，採頁面置中、155 mm 寬等比例顯示；
規範沒有另定精確尺寸。封面、審定書及封底不額外加浮水印，
誌謝起至附錄均有。來源與用途見 [assets/README.md](assets/README.md)。

## 自行驗證

需 Python 3 的 pdfplumber、pypdf，以及 Poppler 的 pdftoppm、pdfinfo、pdffonts。
這些只用於檢查，不是編譯論文的依賴。

~~~sh
python3 -m pip install pdfplumber pypdf
python3 scripts/verify_pdf.py --report tmp/pdfs/metrics.json
mkdir -p tmp/pdfs
pdftoppm -scale-to 1250 -png output/pdf/main.pdf tmp/pdfs/main
pdffonts output/pdf/main.pdf
~~~

量測腳本針對交付示例及其關鍵文字設計；改成自己的論文後，
頁數和示例定位可能變動，請更新相關檢查或人工核對，不能只憑腳本通過宣稱所有論文合規。
視覺檢查還須確認換行、圖表可讀性、標題與圖形相對位置、簽章及實際資料。

## 送印前人工處理

1. 替換所有佔位資料和虛構文獻；核對中英文字、括號、筆畫排序與真實來源。
2. 取得學校正式審定書，完成簽章後填入 ThesisApprovalPDF。
   引入時保留表單，模板會疊上連續羅馬頁碼；需確認表單下方 1 cm 的頁碼區無既有文字，
   並檢查掃描頁數、A4 大小、簽名清晰度。官方表單未提供，本次不能驗證其正式內容。
3. 將 PDF 以 **實際大小／100%**、**雙面長邊翻頁**列印；封面封底材質及裝訂由系所／裝訂店確認。
   若封底需另製，與裝訂店說明 PDF 最後一頁是空白封底，不要擅自改變前置起算。
4. 書背使用獨立 spine.pdf；依實體厚度調整尺寸，長題目需要調小書背字級，共用中文題目不可加入 LaTeX 換行指令。
   必須確認書背仍只有一頁、沒有裁切或溢出，不能直接把 15 mm 當成校方規定。
5. 每次更改資料、圖表、字型或審定書後，重新完成編譯及 PDF 檢視。
