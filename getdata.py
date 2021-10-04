import re
import pandas as pd
import sys

f=open("sample.txt","r")
# p1=re.compile("gg.setValues\(\{(.+?)\}\)gg\.[a-zA-Z]{1,20}\(\)")
p1=re.compile("gg.setValues\(\{(.+?)\}\)gg\.[a-zA-Z]{1,20}\(.*?\)")
p2=re.compile("\['address'\]\s*=\s*(\w+)")
p3=re.compile("\['value'\]\s*=\s*[\"']*([-+]*\w+)[\"']*")
p4=re.compile("\['flags'\]\s*=\s*[\"']*([-+]*\w+)[\"']*")
text=str(f.read())
text=text.replace("\n","")
text=text.replace("\t","")
text=text.replace(" ","")
results=re.findall(p1,text)
print(results)
extracted_data=[]
for r in results:
    addresses=re.findall(p2,r)
    values=re.findall(p3,r)
    flags=re.findall(p4,r)
    extracted_data.append({"addresses":list(addresses),"values":list(values),"flags":list(flags)})
extracted_data2=[] 
for a in extracted_data:
    d={"base_address":"","values":"","flags":""}
    d["base_address"]=a["addresses"][0]
    for v in a["values"]:
        d["values"]=d["values"]+" "+v.rstrip("r")
    d["values"]=d["values"].strip(" ")
    for f in a["flags"]:
        d["flags"]=d["flags"]+" "+f
        d["flags"]=d["flags"].strip(" ")
    extracted_data2.append(d)
        
df=pd.DataFrame(extracted_data2)
df.to_csv("extracted_data.csv",index=False)

template_format1='gg.setRanges(gg.REGION_CODE_APP)\nname("libtersafe.so")\noffset = 0x# \noriginal("7F 45 4C 46 01 01 01 00")\nreplaced("$")\ngg.clearResults()'
template_format2='py = #\nsetvalue(tu + py, & , $)'

def append_new_line(file_name, text_to_append):
    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n\n")
        file_object.write(text_to_append)

if __name__ == "__main__":
    if sys.argv[1]=="t1":
        for v in extracted_data2:
            template=template_format1.replace("$",v["values"])
            template=template.replace("#",(v["base_address"]).lstrip("0x40"))
            append_new_line("sampleprogram.txt",template)
    
    if sys.argv[1]=="t2":
        for v in extracted_data2:
            template=template_format2.replace("$",v["values"])
            template=template.replace("#",(v["base_address"]))
            template=template.replace("&",v["flags"])
            append_new_line("sampleprogram.txt",template)
            


