def calc_avg(count, t_count):
    if t_count <= 0:
        return 0
    avg = count/t_count
    return round(avg, 2) # 2.53

def calc_cfr(n_issues, n_deps):
    if n_deps <= 0:
        return 0
    cfr = (n_issues / n_deps) * 100
    return round(cfr, 2) # 22.12

def calc_cfr_hotfix_to_release(n_releases, n_hotfxies):
    if n_releases <= 0:
        return 0
    cfr = calc_cfr(n_hotfxies , n_releases)
    return cfr 

def calc_cfr_bugs_to_tasks_ratio(prev_ratio, n_releases, n_total_tickets, n_failures):
    if n_total_tickets <= 0:
        return 0    
    prev_ratio_and_release = float(prev_ratio) * int(n_releases)
    output = prev_ratio_and_release + calc_cfr(n_failures , n_total_tickets)
    cfr = output / n_releases + 1
    return round(cfr,2) 

def calc_cfr_bug_to_feature(prev_ratio, n_releases, n_features, n_bugs):
    if n_features <= 0:
        return 0
    prev_ratio_and_release = float(prev_ratio) * int(n_releases)
    output = prev_ratio_and_release + calc_cfr(n_bugs , n_features)
    cfr = output / n_releases + 1
    return round(cfr,2) 

def calc_cfr_bug_release_ratio(n_releases, n_bugfree_releases):
    if n_releases <= 0:
        return 0
    cfr = calc_cfr(n_bugfree_releases , n_releases)
    return cfr     