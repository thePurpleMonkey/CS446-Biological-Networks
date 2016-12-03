import gzip, urllib.request, threading

# File to download and process.
DATABASE = "http://www.pathwaycommons.org/archives/PC2/current/PathwayCommons.8.All.BINARY_SIF.hgnc.txt.sif.gz"

class AsyncOutput(threading.Thread):
	def __init__(self):
		self.output = 0
		self.running = True

		threading.Thread.__init__(self)

	def run(self):
		try:
			while self.running:
				print("\r" + str(self.output), end="")
		except Exception as e:
			print(e)


interactions = {} 				# Records the number of each type of interaction
total_interactions = 0 			# Records the total number of interactions in the database
pp_interactions = 0				# Records the number of protein-protein interactions in the datbaase
unique_pp_interactions = set() 	# Records which protein pairs interact with each other
pp_participants = set()			# Records individual proteins involved in protein-protein interactions
ao = AsyncOutput()				# Show how many lines have been processed in database

print("Downloading from:", DATABASE)
stream = gzip.GzipFile(fileobj=urllib.request.urlopen(DATABASE))

print("Downloading and processing file. Please be patient, this may take a while.")
ao.start()

try:
	for line in stream:
		line = line.decode()
		ao.output = "Processing line {}".format(total_interactions)
		total_interactions += 1
		protein1, interaction, protein2 = line.strip().split("\t")

		if interaction in interactions:
			interactions[interaction] += 1
		else:
			interactions[interaction] = 1

		if interaction in ("interacts-with", "neighbor-of", "in-complex-with"):
			pp_interactions += 1

			pp_participants.add(protein1)
			pp_participants.add(protein2)
			unique_pp_interactions.add(frozenset((protein1, protein2)))

finally:
	ao.running = False
	ao.join()

print("\rProcessing complete. Results are printed below:\n")
sorted_interactions = reversed(sorted(list(interactions.items()), key=lambda v: v[1]))
print("Interaction type", " " * 13, "Frequency")
print("-" * 40)
for interaction in sorted_interactions:
		print("{:30} {:.4f}".format(interaction[0].replace("-", " "), interaction[1] / total_interactions))

print("\nTotal number of protein-protein interactions: ", pp_interactions)
print("Number of unique protein-protein interactions:", len(unique_pp_interactions))
print("Number of unique proteins participating in a protein-protein interaction:", len(pp_participants))