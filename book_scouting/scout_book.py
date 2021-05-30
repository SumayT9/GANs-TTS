from googlesearch import search

transcribed_text = "hello"

results = search((transcribed_text + " pdf free filetype:pdf"), lang = "en", num_results=5)

print(str(results))