<h1> TODO

1. Create Bash interactions
2. Create Django interactions
3. Combine GO terms with PFAM file Michele gave


<h2> Nice to haves

- If given directory link, find first .fna link in directory and use that.
- Graphical interface
- If random .fna link, how do I find the name?
- Docker-ized containers
- Add options for each of the pipeline stages
- Keep log of which hmms were used to analyze which organisms
- Clean script with removes binaries and other space intensive programs
- Add loading screen detailing what is happening

Try awk for csv change

cat results/Clostridium_botulinum_A_Hall_uid19521/hmm_out.txt.test | awk '{print $1"," $5}'

