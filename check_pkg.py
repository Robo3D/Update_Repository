#!/usr/bin/python
import os
from subprocess import Popen, PIPE
import logging
import os.path
import json

logging.basicConfig(filename='/var/log/server_pkg.log', level=logging.INFO)


def unique(lst):
    s = {}
    [s.__setitem__(repr(p), p) for p in lst]
    return s.values()


class Repository():
	"""
	Check new update package.
	"""

	def __init__(self):
		self.path = "/var/www/repos/apt/debian"

	def _reprepro(self, args):
		os.chdir(self.path)
		p = Popen(['/usr/bin/reprepro', '-Vb.'] + args.split(' '), stdout=PIPE, stderr=PIPE)
		return (p.communicate(), p.returncode)

	def get_packages(self, dist):
		try:
			results = {}
			distdir = os.path.join(self.path, 'dists/%s' % dist)
			for dirpath, dirnames, filenames in os.walk(distdir):
				for name in filenames:
					if name != 'Packages': continue
					path = os.path.join(dirpath, name)
					packages = file(path, 'r').read()
					packages = packages.split('\n\n')
					for pkg in packages:
						fields = []
						for field in pkg.split('\n'):
							if not field: continue
							if field[0].isalpha():
								fields.append(field.split(': ', 1))
							else:
								fields[-1][1] += field
						if not fields:
							continue
						pkg = dict(fields)
						pkgname = pkg['Package']
						if not pkgname in results:
							results[pkgname] = []
							results[pkgname].append(pkg)
			# print 'results: {}'.format(results)
			pkg_lists = results.keys()
			pkgs = {'Jessie': []}
			for item in pkg_lists:
				pkgs['Jessie'].append({'pkg': item, 'version': results[item][0]["Version"]})

			logging.info('pkgs: {}'.format(pkgs))
			print('pkgs: {}'.format(pkgs))

			json_data = json.dumps(pkgs)

			return json_data

		except Exception as e:

			print 'Error: {}'.format(e)
			return []

	def get_package(self, dist, package):
		p = self.get_packages(dist)
		return unique(p.get(package, []))


if __name__ == '__main__':
	repos = Repository()
	repos.get_packages('Jessie')