rem 执行改批处理前先要目录下创建font_properties文件

echo Run Tesseract for Training..

tesseract.exe mydit_bi.font.exp0.tif mydit_bi.font.exp0 -l eng --psm 6 nobatch box.train

echo Compute the Character Set..

unicharset_extractor.exe mydit_bi.font.exp0.box

mftraining -F font_properties -U unicharset -O mydit_bi.unicharset mydit_bi.font.exp0.tr

echo Clustering..

cntraining.exe mydit_bi.font.exp0.tr

echo Rename Files..

rename normproto mydit_bi.normproto

rename inttemp mydit_bi.inttemp

rename pffmtable mydit_bi.pffmtable

rename shapetable mydit_bi.shapetable

echo Create Tessdata..

combine_tessdata.exe mydit_bi.