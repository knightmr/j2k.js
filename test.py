import os, sys, re, json, shutil
from subprocess import Popen, PIPE, STDOUT

exec(open(os.path.expanduser('~/.emscripten'), 'r').read())

sys.path.append(EMSCRIPTEN_ROOT)
import tools.shared as emscripten

data = str(map(ord, open('syntensity_lobby_s.j2k', 'r').read()))
output = emscripten.run_js(SPIDERMONKEY_ENGINE, 'test.js', [data, sys.argv[1]])
#print output
m = re.search("result:(.*)", output)
assert m, 'Failed to generate proper output: %s' % output
output = eval('[' + m.groups(1)[0] + ']')
width = output[0]
height = output[1]
data = ''.join([chr(item) for item in output[2:]])

out = open('generated.raw', 'wb')
out.write(data)
out.close()

# check

assert width == 40, 'Failed to generate proper width: %d' % width
assert height == 30, 'Failed to generate proper height: %d' % height

reference = open('reference.raw', 'rb').read()
assert reference == data, 'Failed to generate proper output :('

print 'Success :)'

