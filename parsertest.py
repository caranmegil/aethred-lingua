import lingua

brain = lingua.parse('aethred.xml')
print(brain.patterns[1].get_response())
