import re

def cvParser(dir=dir):
	cvFile = open(dir, "r")

	lines = []
	cvlinkData = {}

	while True:
		s = cvFile.readline().strip()
		if s == "":
			break
		elif s == "/n":
			continue
		elif s[:2] == "//":
			continue
		elif s == "*** href ***":
			break
		lines.append(s)

	while True:
		s = cvFile.readline().strip()
		if s == "":
			break
		colonPos = s.find(":")
		cvlinkData[s[:colonPos]] = s[colonPos+1:]

	cvFile.close()

	cvData = []
	cvContentParser(lines, cvData, cvlinkData)

	return cvData


def cvContentParser(lines, result, linkData):
	part = {}
	yearContent = {}
	currentYear = ""
	currentTitle = ""
	while len(lines) > 0:
		cline = lines[0]
		if cline[0] == "[":
			if cline[1] == "t":
				title = stringFinder(cline, "t", linkData)
				if len(part) > 1:
					part["year-content"].append(yearContent)
					result.append(part)
					part = {}
					yearContent = {}

				currnetTitle = title
				part["title"] = title
				part["year-content"] = []

			elif cline[1] == "y":
				year = stringFinder(cline, "y", linkData)

				if year != currentYear and len(yearContent) > 0:
					part["year-content"].append(yearContent)
					yearContent = {}

				currentYear = year
				yearContent["year"] = currentYear
				yearContent["content"] = []
			elif cline[1] == "d":
				desc = stringFinder(cline, "d", linkData)
				yearContent["content"].append({"tag":"d", "text":desc})

			elif cline[1] == "c":
				context = stringFinder(cline, "c", linkData)
				yearContent["content"].append({"tag":"c", "text":context})

		else:
			yearContent["content"].append({"tag":"t", "text":cline})

		lines.remove(cline)
	
	part["year-content"].append(yearContent)
	result.append(part)


def stringFinder(s, tag, keywords):

	startString = '\[\s*' + tag + '\s*\s*\]'
	endString = '\[\s*/\s*' + tag + '\s*\]'

	lstartString = '\[\s*l\s*[a-z]+\s*\]'
	lendString = '\[\s*/\s*l\s*\]'

	tagStart = re.search(startString, s, re.IGNORECASE)
	tagEnd = re.search(endString, s, re.IGNORECASE)

	ltagStart = re.search(lstartString, s, re.IGNORECASE)
	ltagEnd = re.search(lendString, s, re.IGNORECASE)
	if ltagStart != None:
		assert(ltagEnd != None)
		ss = s[tagStart.end():tagEnd.start()]
		ltagStart = re.search(lstartString, ss, re.IGNORECASE)
		ltagEnd = re.search(lendString, ss, re.IGNORECASE)
		result = ""
		while ltagStart != None:
			keyword = ltagStart.group().replace(" ", "")[2:-1]
			linkedString = ss[ltagStart.end():ltagEnd.start()]
			result += ss[:ltagStart.start()] + '<a href=' + keywords[keyword] + ' target="blank">' + linkedString + '</a>'
			ss = ss[ltagEnd.end()+1:]
			ltagStart = re.search(lstartString, ss, re.IGNORECASE)
			ltagEnd = re.search(lendString, ss, re.IGNORECASE)

		return result
	else:
		return s[tagStart.end():tagEnd.start()]
