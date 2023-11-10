from prior.p4 import work_in_links
import os

# ---
project = '/data/project/mdwiki/'
# ---
if not os.path.isdir(project):
    project = '/mdwiki'
# ---
project_json = f'{project}/md_core/prior/json/'


def start_test(links=[]):
    # ---
    if links == []:
        links = ["Syncope (medicine)"]
    # start work in all links
    # ---
    # links.sort()
    # ---
    main_File = project_json + 'test.json'
    main_File_en = project_json + 'en_test.json'
    # ---
    # python3 core8/pwb.py prior/p4 test
    # ---
    work_in_links(links, main_File, main_File_en, Log=False)
    # ---
    # log_all(main_File)
    # log_allen(main_File_en)
    # ---
    return all, allen


# ---
