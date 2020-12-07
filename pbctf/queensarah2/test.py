from string import ascii_lowercase
from itertools import product
from random import SystemRandom
from math import ceil, log

from string import ascii_lowercase
from itertools import product
from random import SystemRandom
from math import ceil, log

random = SystemRandom()
ALPHABET = ascii_lowercase + "_"

bigrams = [''.join(bigram) for bigram in product(ALPHABET, repeat=2)]
random.shuffle(bigrams)

S_box = {}
for i in range(len(ALPHABET)):
    for j in range(len(ALPHABET)):
        S_box[ALPHABET[i]+ALPHABET[j]] = bigrams[i*len(ALPHABET) + j]
#S_box={'aa': 'sp', 'ab': 'ki', 'ac': 'hh', 'ad': 'oy', 'ae': 'uq', 'af': 'yr', 'ag': 'pi', 'ah': 'mx', 'ai': 'ew', 'aj': 'sf', 'ak': 'rj', 'al': 'ji', 'am': 'i_', 'an': 'xt', 'ao': 'oh', 'ap': 'iq', 'aq': 'rn', 'ar': 'sk', 'as': 'ag', 'at': 'py', 'au': 'of', 'av': 'bh', 'aw': 'kz', 'ax': 'zr', 'ay': 'pu', 'az': 'xg', 'a_': 'pe', 'ba': 'pk', 'bb': 'lu', 'bc': 'en', 'bd': 'sz', 'be': '_y', 'bf': 'cq', 'bg': 'k_', 'bh': 'rx', 'bi': 'tg', 'bj': 'na', 'bk': 'ng', 'bl': 'ue', 'bm': 'oe', 'bn': 'dp', 'bo': 'vl', 'bp': 'qj', 'bq': '_f', 'br': 'nr', 'bs': 'mt', 'bt': 'sd', 'bu': 'yt', 'bv': 'll', 'bw': 'lk', 'bx': 'jg', 'by': 'bn', 'bz': 'yj', 'b_': 'hs', 'ca': 'dn', 'cb': 're', 'cc': 'gk', 'cd': 'vs', 'ce': 'fu', 'cf': 'wx', 'cg': 'd_', 'ch': 'ud', 'ci': 'fg', 'cj': 'bg', 'ck': 'xr', 'cl': 'zm', 'cm': 'wh', 'cn': 'aj', 'co': 'dq', 'cp': 'hr', 'cq': 'vq', 'cr': 'vz', 'cs': 'sl', 'ct': 'um', 'cu': 'nk', 'cv': '_u', 'cw': 'on', 'cx': 'g_', 'cy': 'jv', 'cz': 'u_', 'c_': 'sh', 'da': 'l_', 'db': 'am', 'dc': 'qe', 'dd': 't_', 'de': 'oq', 'df': 'pb', 'dg': 'm_', 'dh': 'tf', 'di': 'xj', 'dj': 'wt', 'dk': 'nq', 'dl': 'wu', 'dm': 'kt', 'dn': 'jj', 'do': 'rk', 'dp': 'rg', 'dq': 'gz', 'dr': 'br', 'ds': 'vo', 'dt': 'rf', 'du': 'wg', 'dv': 'sv', 'dw': 'ch', 'dx': 'nl', 'dy': 'iw', 'dz': 'ga', 'd_': 'bb', 'ea': 'as', 'eb': 'bt', 'ec': 'cl', 'ed': 'nm', 'ee': 'ri', 'ef': 'ap', 'eg': 'tt', 'eh': 'qt', 'ei': 'qz', 'ej': 'se', 'ek': 'ay', 'el': 'qo', 'em': 'hq', 'en': 'su', 'eo': 'ff', 'ep': 've', 'eq': 'yo', 'er': 'uz', 'es': 'xu', 'et': 'ik', 'eu': 'ec', 'ev': 'sw', 'ew': 'az', 'ex': 'nd', 'ey': 'ns', 'ez': 'nc', 'e_': 'vw', 'fa': 'xv', 'fb': 'ta', 'fc': 'kd', 'fd': 'ux', 'fe': 'db', 'ff': 'dw', 'fg': 'zl', 'fh': 'yx', 'fi': 'og', 'fj': 'pf', 'fk': 'rq', 'fl': 'at', 'fm': 'fs', 'fn': 'nw', 'fo': 'wb', 'fp': 'lf', 'fq': 'xl', 'fr': 'sq', 'fs': 'uo', 'ft': 'ps', 'fu': 'zp', 'fv': 'es', 'fw': 'ny', 'fx': 'lt', 'fy': 'ms', 'fz': 'dj', 'f_': 'yb', 'ga': 'vi', 'gb': 'bk', 'gc': 'gi', 'gd': 'al', 'ge': 'tl', 'gf': 'af', 'gg': 'km', 'gh': 'cu', 'gi': 'md', 'gj': 'ur', 'gk': 'gx', 'gl': 'fw', 'gm': 'nf', 'gn': 'sb', 'go': 'vm', 'gp': 'mn', 'gq': 'pp', 'gr': 'sj', 'gs': 'dh', 'gt': 'bs', 'gu': 'fa', 'gv': 'v_', 'gw': 'qp', 'gx': 'nn', 'gy': 'zz', 'gz': 'wj', 'g_': 'ky', 'ha': 'yw', 'hb': 'xa', 'hc': 'fd', 'hd': 'iz', 'he': 'a_', 'hf': 'fv', 'hg': 'ci', 'hh': 'vb', 'hi': 'qn', 'hj': 'hn', 'hk': 'ep', 'hl': 'tc', 'hm': 'yn', 'hn': 'os', 'ho': 'ui', 'hp': 'qy', 'hq': 'mb', 'hr': 'yp', 'hs': 'du', 'ht': 'mp', 'hu': 'lv', 'hv': 'ig', 'hw': 'nv', 'hx': 'gr', 'hy': 'ht', 'hz': '_p', 'h_': 'tw', 'ia': 'an', 'ib': 'vp', 'ic': 'cr', 'id': 'ko', 'ie': 'dr', 'if': 'ul', 'ig': 'b_', 'ih': 'hy', 'ii': 'xy', 'ij': 'cy', 'ik': 'qv', 'il': 'cd', 'im': 'pl', 'in': 'kq', 'io': 'j_', 'ip': 'dc', 'iq': 'cp', 'ir': 'dl', 'is': 'px', 'it': 'sx', 'iu': 'uv', 'iv': 'wz', 'iw': 'fe', 'ix': 'xk', 'iy': 'mz', 'iz': 'do', 'i_': 'td', 'ja': 'vc', 'jb': 'vh', 'jc': 'gp', 'jd': 'e_', 'je': 'fq', 'jf': 'lq', 'jg': 'ee', 'jh': 'uc', 'ji': 'z_', 'jj': 'eo', 'jk': 'w_', 'jl': 'ei', 'jm': 'kw', 'jn': 's_', 'jo': 'li', 'jp': 'yq', 'jq': 'uh', 'jr': 'xp', 'js': 'tk', 'jt': 'ze', 'ju': 'go', 'jv': '_s', 'jw': '_q', 'jx': 'pd', 'jy': 'gy', 'jz': 'po', 'j_': 'cg', 'ka': 'qm', 'kb': 'uj', 'kc': 'la', 'kd': 'da', 'ke': 'bc', 'kf': 'fr', 'kg': 'df', 'kh': 'ej', 'ki': 'mf', 'kj': 'nu', 'kk': 'le', 'kl': 'wp', 'km': 'yi', 'kn': 'ww', 'ko': 'cv', 'kp': 'sm', 'kq': 'th', 'kr': 'ti', 'ks': 'zu', 'kt': 'ow', 'ku': 'pw', 'kv': 'ls', 'kw': 'mk', 'kx': 'cb', 'ky': 'gn', 'kz': 'h_', 'k_': 'zj', 'la': 'gg', 'lb': '__', 'lc': 'zk', 'ld': 'mu', 'le': 'zw', 'lf': 'mv', 'lg': 'pj', 'lh': 'di', 'li': 'to', 'lj': 'jz', 'lk': 'vk', 'll': 'xn', 'lm': 'ry', 'ln': 'us', 'lo': 'nt', 'lp': 'ib', 'lq': 'ez', 'lr': 'sg', 'ls': 'hd', 'lt': 'cc', 'lu': 'ha', 'lv': 'ic', 'lw': 'gq', 'lx': 'om', 'ly': 'el', 'lz': 'kf', 'l_': 'qk', 'ma': 'rl', 'mb': 'if', 'mc': 'vj', 'md': 'eu', 'me': 'yy', 'mf': 'pm', 'mg': 'mq', 'mh': 'rv', 'mi': 'bm', 'mj': 'hc', 'mk': 'ys', 'ml': 'he', 'mm': 'un', 'mn': 'rd', 'mo': 'mg', 'mp': 'kc', 'mq': 'ru', 'mr': 'hp', 'ms': 'im', 'mt': 'ts', 'mu': 'tj', 'mv': 'wc', 'mw': 'uy', 'mx': 'vt', 'my': 'zd', 'mz': 'nz', 'm_': 'wr', 'na': 'xq', 'nb': 'nx', 'nc': 'cx', 'nd': 'xm', 'ne': 'st', 'nf': 'qb', 'ng': 'gm', 'nh': '_v', 'ni': 'ir', 'nj': 'zt', 'nk': 'fc', 'nl': 'zo', 'nm': 'qx', 'nn': 'je', 'no': 'va', 'np': 'yl', 'nq': 'cs', 'nr': 'hx', 'ns': 'me', 'nt': 'vd', 'nu': 'hz', 'nv': '_i', 'nw': 'nh', 'nx': 'zq', 'ny': 'ge', 'nz': 'yc', 'n_': 'dt', 'oa': 'no', 'ob': 'ak', 'oc': 'in', 'od': 'y_', 'oe': 'sy', 'of': 'pr', 'og': 'ca', 'oh': 'zs', 'oi': 'gw', 'oj': 'sn', 'ok': 'ne', 'ol': 'qr', 'om': 'or', 'on': 'tp', 'oo': 'vv', 'op': 'kg', 'oq': 'aw', 'or': 'yk', 'os': 'za', 'ot': 'qw', 'ou': 'jp', 'ov': 'tx', 'ow': 'oz', 'ox': 'hb', 'oy': 'rt', 'oz': 'lz', 'o_': 'jk', 'pa': 'tn', 'pb': 'rp', 'pc': 'jh', 'pd': 'fj', 'pe': '_t', 'pf': 'pc', 'pg': 'bq', 'ph': 'fn', 'pi': 'lg', 'pj': 'sa', 'pk': 'dk', 'pl': 'zx', 'pm': 'hm', 'pn': 'hg', 'po': 'ce', 'pp': 'it', 'pq': '_h', 'pr': 'tm', 'ps': 'qf', 'pt': 'ov', 'pu': 'wi', 'pv': 'fp', 'pw': 'bu', 'px': 'jb', 'py': '_d', 'pz': 'ea', 'p_': 'mj', 'qa': 'zv', 'qb': 'mm', 'qc': 'ty', 'qd': 'ld', 'qe': 'ef', 'qf': 'wd', 'qg': 'ev', 'qh': 'rr', 'qi': 'ol', 'qj': 'jr', 'qk': 'gf', 'ql': 'mw', 'qm': 'xc', 'qn': 'ey', 'qo': 'jm', 'qp': 'ac', 'qq': 'ii', 'qr': 'ye', 'qs': 'xb', 'qt': 'pv', 'qu': 'fi', 'qv': 'av', 'qw': 'cn', 'qx': 'n_', 'qy': 'bz', 'qz': 'lb', 'q_': 'tv', 'ra': '_l', 'rb': 'vg', 'rc': 'gd', 'rd': 'ju', 're': 'qs', 'rf': 'pn', 'rg': 'fm', 'rh': 'gb', 'ri': 'et', 'rj': 'ss', 'rk': 'ft', 'rl': 'ja', 'rm': 'kh', 'rn': 'ad', 'ro': 'ix', 'rp': 'ra', 'rq': 'lm', 'rr': 'mr', 'rs': 'zi', 'rt': 'bw', 'ru': 'uk', 'rv': 'vx', 'rw': 'lr', 'rx': 'gs', 'ry': 'lw', 'rz': 'cz', 'r_': 'cm', 'sa': 'ku', 'sb': 'my', 'sc': 'q_', 'sd': 'tz', 'se': 'fy', 'sf': 'r_', 'sg': 'ax', 'sh': 'ih', 'si': 'rb', 'sj': 'mi', 'sk': 'ya', 'sl': 'wm', 'sm': 'gj', 'sn': 'bf', 'so': 'oo', 'sp': 'hu', 'sq': 'xh', 'sr': 'kn', 'ss': '_w', 'st': 'bp', 'su': 'uw', 'sv': 'up', 'sw': 'zf', 'sx': 'te', 'sy': 'zc', 'sz': '_c', 's_': 'eb', 'ta': 'hf', 'tb': 'ka', 'tc': 'tb', 'td': 'bo', 'te': 'ds', 'tf': 'uf', 'tg': 'id', 'th': 'lh', 'ti': 'jo', 'tj': 'jq', 'tk': 'ph', 'tl': 'dd', 'tm': 'wv', 'tn': 'pz', 'to': 'dg', 'tp': '_j', 'tq': 'pa', 'tr': 'yu', 'ts': 'bl', 'tt': 'dy', 'tu': 'xz', 'tv': 'dv', 'tw': 'bj', 'tx': 'nb', 'ty': 'co', 'tz': 'fb', 't_': 'hl', 'ua': 'qc', 'ub': 'au', 'uc': 'kv', 'ud': 'vu', 'ue': 'ct', 'uf': 'eg', 'ug': 'tu', 'uh': 'ex', 'ui': 'zh', 'uj': 'cw', 'uk': 'jc', 'ul': 'vy', 'um': '_g', 'un': 'is', 'uo': 'hj', 'up': 'zb', 'uq': 'ua', 'ur': 'ie', 'us': 'jx', 'ut': 'ug', 'uu': 'wl', 'uv': 'jl', 'uw': 'qh', 'ux': 'bx', 'uy': 'em', 'uz': 'ly', 'u_': 'ok', 'va': 'hi', 'vb': 'rc', 'vc': 'lo', 'vd': 'yz', 've': 'mo', 'vf': 'ah', 'vg': 'fh', 'vh': 'oa', 'vi': 'lp', 'vj': 'ml', 'vk': 'ed', 'vl': 'ks', 'vm': '_z', 'vn': 'ab', 'vo': 'gu', 'vp': 'pq', 'vq': 'dz', 'vr': 'kl', 'vs': 'od', 'vt': 'vr', 'vu': 'rw', 'vv': '_n', 'vw': 'ub', 'vx': 'ma', 'vy': 'np', 'vz': 'eq', 'v_': 'c_', 'wa': 'lc', 'wb': 'ao', 'wc': 'vf', 'wd': 'kk', 'we': 'zg', 'wf': 'x_', 'wg': 'ck', 'wh': 'gc', 'wi': 'xd', 'wj': 'lx', 'wk': 'cj', 'wl': 'rs', 'wm': 'o_', 'wn': 'pg', 'wo': 'yh', 'wp': 'si', 'wq': 'ob', 'wr': 'xs', 'ws': 'f_', 'wt': '_r', 'wu': 'hw', 'wv': 'qi', 'ww': 'rz', 'wx': 'er', 'wy': 'yg', 'wz': 'ij', 'w_': 'qu', 'xa': 'mc', 'xb': 'wy', 'xc': 'lj', 'xd': 'il', 'xe': 'xo', 'xf': 'jt', 'xg': 'de', 'xh': 'iy', 'xi': 'xw', 'xj': 'aq', 'xk': 'kx', 'xl': 'gl', 'xm': 'fk', 'xn': 'ba', 'xo': 'yf', 'xp': 'wn', 'xq': 'xe', 'xr': 'so', 'xs': '_a', 'xt': 'ip', 'xu': 'we', 'xv': 'yv', 'xw': '_o', 'xx': 'zy', 'xy': 'io', 'xz': 'oj', 'x_': 'js', 'ya': 'xf', 'yb': 'ni', 'yc': 'gv', 'yd': 'qa', 'ye': 'jn', 'yf': 'ro', 'yg': 'sr', 'yh': '_k', 'yi': 'ke', 'yj': 'nj', 'yk': 'ut', 'yl': 'jw', 'ym': '_b', 'yn': 'kp', 'yo': 'iv', 'yp': 'kb', 'yq': 'op', 'yr': 'cf', 'ys': 'ai', 'yt': 'rm', 'yu': 'ln', 'yv': 'fl', 'yw': 'hk', 'yx': 'kj', 'yy': 'ot', 'yz': 'ek', 'y_': 'wk', 'za': 'eh', 'zb': 'pt', 'zc': 'ou', 'zd': 'yd', 'ze': 'kr', 'zf': 'tq', 'zg': 'gh', 'zh': 'qq', 'zi': 'dx', 'zj': 'qg', 'zk': 'bv', 'zl': 'be', 'zm': 'jy', 'zn': 'vn', 'zo': 'oc', 'zp': 'bd', 'zq': 'uu', 'zr': '_e', 'zs': 'ox', 'zt': 'ws', 'zu': 'sc', 'zv': 'wo', 'zw': 'wq', 'zx': 'tr', 'zy': 'gt', 'zz': 'fo', 'z_': 'aa', '_a': 'wa', '_b': 'oi', '_c': 'ho', '_d': 'ym', '_e': '_x', '_f': '_m', '_g': 'iu', '_h': 'ar', '_i': 'xi', '_j': 'p_', '_k': 'hv', '_l': 'rh', '_m': 'qd', '_n': 'mh', '_o': 'jf', '_p': 'ae', '_q': 'fx', '_r': 'fz', '_s': 'jd', '_t': 'zn', '_u': 'bi', '_v': 'ia', '_w': 'wf', '_x': 'by', '_y': 'xx', '_z': 'ql', '__': 'dm'}
assert len(set(S_box.keys())) == 27*27

def encrypt(message):
    if len(message) % 2:
        message += "_"

    message = list(message)
    rounds = int(2 * ceil(log(len(message), 2))) # The most secure amount of rounds

    for round in range(rounds):
        # Encrypt
        for i in range(0, len(message), 2):
            message[i:i+2] = S_box[''.join(message[i:i+2])]

        # Shuffle, but not in the final round
        if round < (rounds-1):
            message = [message[i] for i in range(len(message)) if i%2 == 0] + [message[i] for i in range(len(message)) if i%2 == 1]

    return ''.join(message)

bigrams = [''.join(bigram) for bigram in product(ALPHABET, repeat=2)]
while(len(bigrams) != 0):
    tmp0 = bigrams[0]
    tmp1 = tmp0
    tmp = []
    while(True):
        bigrams.remove(tmp1)
        tmp.append(tmp1)
        tmp1 = S_box[tmp1]
        if tmp1 == tmp0:
            print(len(tmp))
            break

