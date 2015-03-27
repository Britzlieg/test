# encoding:utf-8
__author__ = 'zhijieli'
# import re
#
# txt = "note.txt"
# out = 'data.txt'
#
# f = open(txt,'r')
# txt_data = f.read()
# f.close()
#
# regex = "{name: '(.*)',"
# p = re.compile(regex)
# res = p.findall(txt_data)
#
# out_data = ''
# for i in range(0,len(res)):
#     tpl = "$city['" + res[i] + "'] = 0;\n"
#     out_data = out_data + tpl;
#
# f = open(out,'w')
# f.write(out_data)
# f.close()




import re

txt = "note.txt"
out = 'data.txt'

f = open(txt,'r')
txt_data = f.read()
f.close()

regex = '$china\[\] = "(.*)";'
p = re.compile(regex)
res = p.findall(txt_data)

out_data = ''
for i in range(0,len(res)):
    tpl = "$province['" + res[i] + "'] = 0;\n"
    out_data = out_data + tpl;

f = open(out,'w')
f.write(out_data)
f.close()