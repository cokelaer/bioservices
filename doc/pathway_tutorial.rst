[(x['graphid'], x['textlabel'],x['type']) for x in bs.findAll("datanode") if
x['type'] == "Protein"]
history

In [90]: bs = bs4.BeautifulSoup(res[0])
KeyboardInterrupt - Ctrl-C again for new prompt


In [91]: res = w.getPathway("WP437")

