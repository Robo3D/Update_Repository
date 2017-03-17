import json
from reposclass import *

base_dir = "/var/www/repos/apt/debian"
repository = Repository(base_dir)
codenames = repository.list_dists()
print codenames