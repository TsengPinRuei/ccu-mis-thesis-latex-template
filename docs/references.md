# 引文與參考文獻

依據：`format.pdf` 第 6 頁 (10-10)。同一處文內引文先英文後中文；文末先中文後英文；中文按作者姓氏筆畫由少至多，英文依作者字母排序；書寫格式參考 APA 7。

## 資料與指令

在 `references.bib` 維護資料，在主檔載入 `ccu-bibliography` 後使用：

```tex
\addbibresource{references.bib}
% 中文段落：全形括號；輸入順序可任意，輸出英先中後。
\ccucite{lin2023,brown2023,wang2024,adams2022}
% 一般 APA 括號引文與敘述式引文：
\parencite{brown2023,adams2022}
\textcite{adams2022}
% 可附頁碼：
\ccucite[25]{wang2024}
% 依 format.pdf 第 1 頁文件組成順序，放在正文之後、附錄之前：
\ccureferences
```

示例多筆引文應為「（Adams, 2022; Brown & Smith, 2023; 王範例, 2024; 林示例, 2023）」；文末順序為王、林、Adams、Brown。

中文資料必須有 `keywords={chinese}` 及人工核對的 `sortkey`。本例 `004001` 表示王姓四畫、該筆畫群的第 1 位作者；`008001` 表示林姓八畫、第 1 位作者。六位數只是易維護的預設，並非學校指定編碼；其用途僅為記錄人工確認的作者排序。同一作者的所有文獻沿用相同 `sortkey`，再由樣式依年份與題名排序。學校未指定同筆畫不同姓氏的次序，請保持一致並與指導教授確認。英文資料不填 `sortkey`，由 Biber 依作者自動排序。

以 `author={{王範例}}` 保留中文姓名完整順序；多位中文作者可寫成 `author={{王範例} and {林示例}}`。所有中文文獻都需標記，漏標者會被當成英文組。混合語言作者、譯著、特殊文獻型別與來源資料的 APA 正確性仍需人工核對。

`ccu-bibliography.sty` 使用 `biblatex-apa` 的 APA 7 格式，保留作者、年份、書籍斜體、期刊卷期與頁碼規則。文末按中文／英文分成連續兩組，不增加分組標題；採 0.5 英吋懸掛縮排（APA 樣式預設），並依學校正文規則設為 12 bp 字、18 bp 基線。全形引文括號及人工排序碼是明示的模板預設。主模板以同一標楷體 Regular 字型搭配 `AutoFakeSlant=.2` 與 `AutoFakeBold=2` 衍生中文斜體與粗體，供規定的圖表標示及斜體內容使用；這些是明示的合成樣式，並非字型原生粗斜體。英文使用 Times New Roman 的真正粗體與斜體字型。中文書名的呈現請依指導教授採用的中文 APA 慣例人工確認。

## 編譯

需 XeLaTeX、Biber、`biblatex` 與 `biblatex-apa` 的相容版本。先編譯主檔產生 `.bcf`，再執行 Biber，最後兩次 XeLaTeX；專案建置腳本會處理完整流程。不要改用 BibTeX。

示例中的作者、出版社、期刊、書名與文章均為清楚標示的虛構佔位資料，不能作為真實研究來源。模板只能處理提供的欄位與樣式，不能證明來源真實、引用充分或原始資料正確。

## 已完成的獨立驗證

2026-09-24 使用 XeLaTeX（TeX Live 2025）、Biber 2.21 完成一次 XeLaTeX、一次 Biber、兩次 XeLaTeX 的獨立範例編譯；最後一輪 LaTeX 與 Biber 紀錄無警告或錯誤。實際 PDF 的括號式及敘述式引文順序均為 Adams、Brown、王、林，參考文獻順序為王、林、Adams、Brown；已檢視頁面影像確認引文分隔符及懸掛縮排。

以 pdfplumber 查核獨立範例參考文獻：字級 12.000 PDF point、相同字型的相鄰基線差 18.000 point，續行與首行起點差 36.000 point（0.5 英吋）。字型清單確認嵌入 Times New Roman（含真正英文斜體）與 DFKaiShu-SB。整份論文的最終頁次與章節版面另見主驗證報告。
