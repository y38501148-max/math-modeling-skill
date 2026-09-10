#!/usr/bin/env python3
"""Original, bounded teaching implementations; see references/algorithm-lab.md.
Requires NumPy/SciPy; the --out report additionally requires Matplotlib.
No source datasets or upstream program code are bundled.
"""
import argparse
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import Bounds, LinearConstraint, linprog, milp


def finite_array(x, ndim=None):
    a = np.asarray(x, dtype=float)
    if not a.size or not np.isfinite(a).all() or (ndim is not None and a.ndim != ndim):
        raise ValueError('nonempty finite array of required dimension expected')
    return a


def ahp(a):
    a = finite_array(a, 2)
    n = len(a)
    if a.shape != (n, n) or (a <= 0).any() or not np.allclose(a * a.T, 1):
        raise ValueError('positive reciprocal square matrix required')
    eigenvalues, vectors = np.linalg.eig(a)
    k = np.argmax(eigenvalues.real)
    w = np.abs(vectors[:, k].real)
    w /= w.sum()
    ci = max(0., (eigenvalues[k].real - n) / (n - 1)) if n > 1 else 0.
    ri = {3: .58, 4: .90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
    return w, ci, ci / ri[n] if n in ri else None


def topsis(x, benefit, weights):
    """Min-max direction alignment; constant columns contribute no discrimination."""
    x = finite_array(x, 2)
    w = finite_array(weights, 1)
    b = np.asarray(benefit, dtype=bool)
    if len(w) != x.shape[1] or b.shape != w.shape or (w < 0).any() or w.sum() <= 0:
        raise ValueError('one nonnegative weight and direction per column required')
    span = np.ptp(x, axis=0)
    z = (x - x.min(axis=0)) / np.where(span == 0, 1, span)
    z[:, ~b] = 1 - z[:, ~b]
    z[:, span == 0] = 0
    v = z * (w / w.sum())
    good = np.linalg.norm(v - v.max(axis=0), axis=1)
    bad = np.linalg.norm(v - v.min(axis=0), axis=1)
    total = good + bad
    return np.divide(bad, total, out=np.full(len(x), .5), where=total > 0)


def pcr_fit(x, y, components):
    x, y = finite_array(x, 2), finite_array(y, 1)
    if len(x) != len(y) or len(x) < 2:
        raise ValueError('aligned training observations required')
    center, scale = x.mean(axis=0), x.std(axis=0, ddof=1)
    scale = np.where(scale == 0, 1, scale)
    z = (x-center)/scale
    _, s, vt = np.linalg.svd(z, full_matrices=False)
    rank = np.linalg.matrix_rank(z)
    if not isinstance(components, int) or not 1 <= components <= rank:
        raise ValueError('component count must not exceed training rank')
    axes = vt[:components].T  # no sign(sum(column)): zero-sum axes are valid
    coef = np.linalg.lstsq(z @ axes, y-y.mean(), rcond=None)[0]
    beta = axes @ coef / scale
    return dict(beta=beta, intercept=y.mean()-center@beta, center=center, scale=scale, axes=axes)


def pcr_predict(model, x):
    return finite_array(x, 2) @ model['beta'] + model['intercept']


def gm11(y, horizon=1):
    y = finite_array(y, 1)
    if len(y) < 4 or (y <= 0).any() or not isinstance(horizon, int) or horizon < 0:
        raise ValueError('at least four positive observations and nonnegative horizon required')
    accumulated = np.cumsum(y)
    design = np.column_stack((-(accumulated[:-1]+accumulated[1:])/2, np.ones(len(y)-1)))
    a, b = np.linalg.lstsq(design, y[1:], rcond=None)[0]
    t = np.arange(len(y)+horizon, dtype=float)
    if abs(a) < 1e-10:
        fitted = np.r_[y[0], np.full(len(t)-1, b)]
    else:
        acc = y[0]*np.exp(-a*t) - b*np.expm1(-a*t)/a
        fitted = np.r_[y[0], np.diff(acc)]
    if not np.isfinite(fitted).all():
        raise ValueError('unstable grey extrapolation')
    return fitted


def moving_average_next(y, window):
    y = finite_array(y, 1)
    if not isinstance(window, int) or not 1 <= window <= len(y):
        raise ValueError('window out of range')
    return float(y[-window:].mean())


def floyd(dist):
    """np.inf means absent edge; zero and negative weights are supported."""
    d = np.asarray(dist, dtype=float).copy()
    if d.ndim != 2 or d.shape[0] != d.shape[1] or not len(d) or np.isnan(d).any() or np.isneginf(d).any():
        raise ValueError('square adjacency with finite weights or +inf required')
    np.fill_diagonal(d, np.minimum(np.diag(d), 0))
    for k in range(len(d)):
        d = np.minimum(d, d[:, k, None]+d[None, k, :])
    if (np.diag(d) < -1e-12).any():
        raise ValueError('negative cycle')
    return d


def max_flow(capacity, source, sink):
    """Edmonds-Karp, skew-symmetric net flow; supports antiparallel capacities."""
    c = finite_array(capacity, 2)
    n = len(c)
    if c.shape != (n, n) or (c < 0).any() or source == sink or not 0 <= source < n or not 0 <= sink < n:
        raise ValueError('invalid capacity or terminal')
    f = np.zeros_like(c)
    while True:
        parent = np.full(n, -1, dtype=int)
        parent[source] = source
        queue = deque([source])
        while queue and parent[sink] == -1:
            u = queue.popleft()
            for v in np.flatnonzero(c[u]-f[u] > 1e-12):
                if parent[v] == -1:
                    parent[v] = u
                    queue.append(v)
        if parent[sink] == -1:
            reachable = parent != -1
            return float(f[source].sum()), f, reachable
        v, amount = sink, np.inf
        while v != source:
            u = parent[v]; amount = min(amount, c[u,v]-f[u,v]); v = u
        v = sink
        while v != source:
            u = parent[v]; f[u,v] += amount; f[v,u] -= amount; v = u


def route_cost(d, route):
    return float(sum(d[route[i-1], route[i]] for i in range(len(route))))


def anneal_tour(d, seed=7, proposals=2000):
    d = finite_array(d, 2)
    n = len(d)
    if d.shape != (n,n) or n < 3 or proposals < 1:
        raise ValueError('square complete graph, >=3 nodes and positive budget required')
    rng = np.random.default_rng(seed)
    current = np.arange(n); best = current.copy()
    current_cost = best_cost = route_cost(d, current)
    trace = [best_cost]
    for step in range(proposals):
        temperature = max(float(d.max()), 1e-6) * (.001 ** (step/proposals))
        candidate = current.copy()
        i,j = rng.choice(np.arange(1,n), 2, replace=False)
        candidate[i],candidate[j] = candidate[j],candidate[i]
        cost = route_cost(d,candidate)
        if cost < current_cost or rng.random() < np.exp(min(0., (current_cost-cost)/temperature)):
            current, current_cost = candidate, cost
            if cost < best_cost:
                best, best_cost = candidate.copy(), cost
        trace.append(best_cost)
    return best, route_cost(d,best), np.asarray(trace)


def traffic_step(cells):
    """Periodic one-lane deterministic exclusion CA, one-cell speed, synchronous."""
    old = np.asarray(cells)
    if old.ndim != 1 or len(old) < 2 or not np.isin(old,[0,1]).all():
        raise ValueError('binary ring required')
    old = old.astype(int)
    moving = (old == 1) & (np.roll(old,-1) == 0)
    return old - moving + np.roll(moving,1)


def heat_error(n, end=.1):
    """u_t=u_xx, x in [0,1], zero boundaries, u(x,0)=sin(pi*x)."""
    if n < 4 or end <= 0:
        raise ValueError('positive duration and >=4 cells required')
    dx = 1/n; steps = int(np.ceil(end/(.4*dx*dx))); dt = end/steps
    x = np.linspace(0,1,n+1); u = np.sin(np.pi*x); u[[0,-1]] = 0
    for _ in range(steps):
        u[1:-1] += dt/dx**2 * (u[:-2]-2*u[1:-1]+u[2:])
    exact = np.exp(-np.pi**2*end)*np.sin(np.pi*x)
    return float(np.max(np.abs(u-exact)))


def halfpipe(radius=5., flat=0., friction=.02, speed=12., rtol=1e-9):
    """P26-inspired partial model: semicircular side walls, optional flat bottom.
    Solve q=v^2 with y measured upwards: dq/ds=-2g*y'-2mu(g*x'+k*q).
    Parameter values are synthetic. Stops when speed reaches zero.
    """
    if not np.isfinite([radius,flat,friction,speed,rtol]).all() or radius <= 0 or flat < 0 or friction < 0 or speed <= 0 or rtol <= 0:
        raise ValueError('invalid physical parameter')
    g = 9.81; q = speed**2; offset = 0.; samples = []
    arcs = [('left',np.pi*radius/2),('flat',flat),('right',np.pi*radius/2)]
    for kind,length in arcs:
        if length == 0: continue
        def deriv(s,y):
            if kind == 'flat': xp,yp,k = 1.,0.,0.
            else:
                angle = s/radius + (-np.pi/2 if kind=='left' else 0)
                xp,yp,k = np.cos(angle),np.sin(angle),1/radius
            return [-2*g*yp-2*friction*(g*xp+k*y[0])]
        def stop(s,y): return y[0]
        stop.terminal = True; stop.direction = -1
        result = solve_ivp(deriv,(0,length),[q],rtol=rtol,atol=rtol*.01,events=stop,dense_output=True)
        if not result.success: raise RuntimeError(result.message)
        ss = np.linspace(0,result.t[-1],101)
        samples.extend(zip((ss+offset).tolist(),result.sol(ss)[0].tolist()))
        if len(result.t_events[0]):
            return dict(reached_exit=False,exit_speed=None,height=None,trace=np.asarray(samples))
        q = float(result.y[0,-1]); offset += length
    return dict(reached_exit=True,exit_speed=float(np.sqrt(q)),height=q/(2*g),trace=np.asarray(samples))


def run_suite():
    weights,ci,cr = ahp([[1,2,4],[.5,1,2],[.25,.5,1]])
    scores = topsis([[4,8,3],[6,6,3],[8,4,3]],[True,False,True],[1,1,1])
    x = np.arange(1.,21.)
    train = np.column_stack([x,-x])
    model = pcr_fit(train,3+2*x,1)
    pcr_error = float(np.max(np.abs(pcr_predict(model,[[21,-21],[22,-22]])-[45,47])))
    series = 5*np.exp(.04*np.arange(16)); errors = []
    for origin in range(8,16):
        errors.append([gm11(series[:origin],1)[-1]-series[origin],moving_average_next(series[:origin],3)-series[origin]])
    errors = np.asarray(errors)
    c=np.array([-3.,-2.]); a=np.array([[2.,1.],[1.,2.]]); b=np.array([7.,7.])
    lp=linprog(c,A_ub=a,b_ub=b,bounds=(0,None),method='highs')
    integer=milp(c,integrality=np.ones(2),bounds=Bounds(0,np.inf),constraints=LinearConstraint(a,-np.inf,b))
    if not lp.success or not integer.success: raise RuntimeError('optimization did not succeed')
    enumeration=max(3*i+2*j for i in range(8) for j in range(8) if 2*i+j<=7 and i+2*j<=7)
    cap=np.zeros((6,6))
    for u,v in [(0,1),(0,2),(1,3),(1,4),(2,3),(3,5),(4,5)]:cap[u,v]=1
    value,flow,cut=max_flow(cap,0,5)
    distance=floyd([[0,4,5,np.inf],[np.inf,0,-3,np.inf],[np.inf,np.inf,0,0],[np.inf,np.inf,np.inf,0]])
    points=np.array([[0,0],[1,0],[1,1],[0,1],[.5,1.6],[1.5,.5]])
    d=np.linalg.norm(points[:,None]-points[None,:],axis=2)
    optimal=min(route_cost(d,(0,)+p) for p in itertools.permutations(range(1,len(d))))
    tours=[anneal_tour(d,seed=s) for s in range(5)]
    ring=np.array([1,0,1,1,0,0,1,0]); count=int(ring.sum())
    for _ in range(100):ring=traffic_step(ring)
    hs=[heat_error(n) for n in (20,40,80)]
    scenarios=[]
    for flat in [0.,5.,10.]:
        r=halfpipe(flat=flat);fine=halfpipe(flat=flat,rtol=1e-11)
        scenarios.append(dict(flat_m=flat,exit_speed_m_s=r['exit_speed'],height_m=r['height'],tolerance_delta=abs(r['exit_speed']-fine['exit_speed'])))
    return dict(data_status='synthetic teaching examples; P25 values explicitly attributed',
      versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
      script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      evaluation=dict(weights=weights.tolist(),ci=ci,cr=cr,topsis=scores.tolist()),
      pcr=dict(heldout_max_error=pcr_error),forecast=dict(origins=list(range(8,16)),gm_rmse=float(np.sqrt(np.mean(errors[:,0]**2))),moving_average_rmse=float(np.sqrt(np.mean(errors[:,1]**2)))),
      optimization=dict(lp_profit=-float(lp.fun),integer_profit=-float(integer.fun),enumeration_profit=enumeration,integer_x=integer.x.tolist(),max_violation=float(max(0,np.max(a@integer.x-b)))),
      graph=dict(negative_edge_distance=float(distance[0,2]),zero_edge_distance=float(distance[0,3]),max_flow=value,cut_capacity=float(cap[np.ix_(cut,~cut)].sum()),conservation_error=float(np.max(np.abs(flow.sum(axis=1)[1:-1])))),
      search=dict(seeds=list(range(5)),proposals_per_seed=2000,exact_tour=optimal,seed_costs=[r[1] for r in tours],max_gap=max(r[1]-optimal for r in tours)),
      simulation=dict(initial_cars=count,final_cars=int(ring.sum()),heat_errors=hs),
      halfpipe=dict(radius_m=5.,entry_speed_m_s=12.,friction=.02,scenarios=scenarios),
      paper_p25=dict(source='P25 PDF p20 Table8; arithmetic check only',left_ratio=.0136/(.0239+.0518),right_ratio=(.0235+.0207)/.0231,claimed_greater_equal_holds=bool(.0136/(.0239+.0518)>=(.0235+.0207)/.0231)))


def write_report(out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    report=run_suite()
    target=out/'results.json';target.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    fig,axes=plt.subplots(1,2,figsize=(9,3.6),layout='constrained')
    for flat in [0.,5.,10.]:
        r=halfpipe(flat=flat);axes[0].plot(r['trace'][:,0],np.sqrt(np.maximum(0,r['trace'][:,1])),label=f'Flat bottom {flat:g} m')
    axes[0].set(xlabel='Arc length (m)',ylabel='Speed (m/s)',title='Synthetic half-pipe comparison');axes[0].legend(fontsize=8)
    scenarios=report['halfpipe']['scenarios']
    axes[1].bar([str(r['flat_m']) for r in scenarios],[r['height_m'] for r in scenarios],color='#316c86')
    axes[1].set(xlabel='Flat bottom length (m)',ylabel='Ballistic height above exit (m)',title='Fixed side radius and entry speed')
    fig.savefig(out/'halfpipe.png',dpi=180);fig.savefig(out/'halfpipe.svg');plt.close(fig)
    lines=['flat_m,exit_speed_m_s,height_m']+[f"{r['flat_m']},{r['exit_speed_m_s']},{r['height_m']}" for r in scenarios]
    (out/'halfpipe.csv').write_text('\n'.join(lines)+'\n')
    rows='\n'.join(f"| {r['flat_m']:.0f} | {r['exit_speed_m_s']:.4f} | {r['height_m']:.4f} |" for r in scenarios)
    (out/'manuscript.md').write_text('# 半管滑道局部模型：合成参数演示\n\n参考 P26 的能量收支思想，独立求解两段四分之一圆弧与底部直线。半径5 m、入场速度12 m/s、摩擦系数0.02，均为本例设定。令 q=v²，向上为 y 正向：dq/ds=-2g y′-2μ(g x′+κq)。分段积分并在 q=0 停止；出场后按竖直抛射计算 h=q/(2g)。\n\n| 底部长/m | 出场速度/(m/s) | 抛射高度/m |\n|---|---|---|\n'+rows+'\n\n![本次计算结果](halfpipe.png)\n\n固定半径时，增加底部长度降低本例的出场速度；此比较同时改变滑道宽度与总弧长，不能声称普遍最佳设计。未建模主动蹬伸、空气阻力、沿坡运动或旋转，也未复现原论文整题。无摩擦极限保持初末同高速度，收紧积分容差用于数值核验。结果及版本在 results.json，数据在 halfpipe.csv。\n')
    claims=[dict(id=f'height-{i}',artifact='run',pointer=f'/halfpipe/scenarios/{i}/height_m',value=round(r['height_m'],4),abs_tol=.00005,unit='m',status='synthetic',location=f'manuscript table row {i+1}') for i,r in enumerate(scenarios)]
    artifacts=[dict(id='run',path='results.json',sha256=hashlib.sha256(target.read_bytes()).hexdigest())]
    (out/'evidence.json').write_text(json.dumps(dict(version=1,artifacts=artifacts,claims=claims),indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path)
    args=parser.parse_args();result=write_report(args.out) if args.out else run_suite()
    print(json.dumps(result,indent=2,allow_nan=False))
