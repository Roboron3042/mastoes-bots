from common import get_api
from common import list_read

domains_es = [
    "mastodon.uy",
    "chilemasto.casa",
    "mstdn.es",
    "mstdn.mx",
    "sivar.cafe",
    "col.social",
    "mastodon.la",
    "mastodon.cl",
    "seda.social",
    "devschile.social",
    "bizkaia.social",
    "masto.nobigtech.es",
    "masto.es",
    "tkz.one",
    "xarxa.cloud",
    "culturaeinnovacion.social",
    "sindicato.social",
    "hispagatos.space",
    "paquita.masto.host",
    "mastodon.com.py",
    "social.politicaconciencia.org",
    "red.niboe.info",
    "tuiter.rocks",
    "txs.es",
    "lile.cl",
    "bloom.surf",
    "masto.komintern.work",
    "malaga.social",
    "mastodon.cr",
    "oye.social",
    "rebel.ar",
    "mastodon.lajaqueria.org",
    "soymas.to",
    "mst.universoalterno.es",
    "frikiverse.zone",
    "shrimply.social",
    "mast.lat",
    "fediunam.site",
    "mastorol.es",
    "cubatech.social",
    "laterracita.online",
    "41020.social",
    "naturar.social",
    "tu.social",
    "jvm.social",
    "mastodonte.tech",
    "mastodon.escepticos.es",
    "mastodon.mx",
    "ticos.social",
    "mastodon.cr",
    "mastodon.blaster.com.ar",
    "terere.social",
    "andalucia.social",
    "con.tar.mx",
    "cadiz.ovh",
    "irsoluciones.social",
]

domains_regional = [
    "mastodon.eus",
    "mastodon.gal",
    "mastodon.cat",
    "mastodont.cat",
]


def get_domain_list_stats(domains):
    total = 0
    active = 0

    for domain in domains:
        print(domain)
        api = get_api(domain)
        res = api.instance_nodeinfo()
        if domain != "mast.lat": # shared with tkz.one
            total  += res.usage.users.total
        active += res.usage.users.activeMonth
    return [total, active]

def get_other_stats():
    total = 0
    following = list_read("following_accounts.csv")

    for account in following:
        domain = account.split(",")[0].split("@")[1]
        if domain not in domains_es and domain not in domains_regional:
            total += 1
    return total

stats_es = get_domain_list_stats(domains_es)
stats_regional = get_domain_list_stats(domains_regional)
stats_other_total = get_other_stats()

total = stats_es[0] + stats_regional[0] + stats_other_total
total_active = stats_es[1] + stats_regional[1]

print("Estimación de usuarios totales: " + str(stats_es[0]) + " " + str(stats_regional[0]) + " " + str(stats_other_total) + " = " + str(total))
print("Estimación de usuarios activos: " + str(stats_es[1]) + " " + str(stats_regional[1]) + " = " + str(total_active))

