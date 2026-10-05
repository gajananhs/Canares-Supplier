"""Pull POs, Work Orders, GIN and GRN from canaresai.com into transactions.json.
Runs inside GitHub Actions before each deploy. Secrets stay on the server side.
Env: CANARES_API_URL, CANARES_API_TOKEN (or FEED_FILE=path.json for testing).
Expected feed: {"orders":[...], "gin":[...], "grn":[...]}  (see INTEGRATION.md)
"""
import os, re, sys, json, urllib.request
from datetime import datetime, timezone

url, tok, ff = os.environ.get("CANARES_API_URL"), os.environ.get("CANARES_API_TOKEN"), os.environ.get("FEED_FILE")
if not (url or ff):
    print("No CANARES_API_URL configured: sync skipped"); sys.exit(0)
if ff: feed = json.load(open(ff))
else:
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + (tok or ""), "Accept": "application/json"})
    feed = json.load(urllib.request.urlopen(req, timeout=60))

T = json.load(open("transactions.json")); SUP = json.load(open("suppliers.json"))
nk = lambda s: re.sub(r"[^A-Z0-9]", "", str(s or "").upper())
by_id = {s["id"]: s["id"] for s in SUP}; by_name = {nk(s["name"]): s["id"] for s in SUP}
def sup(code, name):
    c = re.sub(r"\s+", "", str(code or "")).upper()
    return by_id.get(c) or by_name.get(nk(name)) or T["alias"].get(nk(name)) or ""
def pick(r, *k, d=""):
    for x in k:
        if r.get(x) not in (None, ""): return r[x]
    return d
def dt(v):
    v = re.sub(r"\bSept\b", "Sep", str(v or "").strip())
    for f in ("%Y-%m-%d", "%d %b %Y", "%d/%m/%Y", "%d-%m-%Y"):
        try: return datetime.strptime(v[:11] if f == "%d %b %Y" else v[:10] if f == "%Y-%m-%d" else v, f).strftime("%Y-%m-%d")
        except ValueError: pass
    return ""
num = lambda v: float(str(v or 0).replace(",", "") or 0)
def replace(kind, rows, key=lambda r: r["no"]):
    nos = {key(r) for r in rows}
    T[kind] = [r for r in T[kind] if r.get("src") != "canaresai" and key(r) not in nos] + rows

orders = []
for o in feed.get("orders", []):
    no = pick(o, "no", "po_no", "work_order_no", "PO No"); s = sup(pick(o, "supplier_code", "Supplier Code"), pick(o, "supplier", "Supplier"))
    typ = "Work Order" if re.search("work", str(pick(o, "type", "Type", d="PO")), re.I) else "Purchase Order"
    for l in o.get("items") or [o]:
        orders.append(dict(no=str(no), type=typ, sup=s, date=dt(pick(o, "date", "PO Date")), due=dt(pick(o, "due", "Due Date")), code=str(pick(l, "code", "Item Code")),
                           name=str(pick(l, "name", "Item Name")), qty=num(pick(l, "qty", "Ordered Qty")), rate=str(pick(l, "rate", "Unit Rate")), src="canaresai"))
replace("po", orders, key=lambda r: r["no"] + "|" + r["code"] + "|" + r["name"])

gin = []
for g in feed.get("gin", []):
    name = pick(g, "supplier", "Supplier")
    gin.append(dict(no=str(pick(g, "no", "GIN No.")), date=dt(pick(g, "date", "Date")), supName=name, sup=sup(pick(g, "supplier_code"), name), po=str(pick(g, "po", "PO No.")), dc=str(pick(g, "dc", "Job Work DC")),
        inv=str(pick(g, "inv", "Invoice No.")), invDate=dt(pick(g, "invDate", "Invoice Date")), veh=str(pick(g, "veh", "Vehicle No.")), gp=str(pick(g, "gp", "Gate Pass No.")),
        rec=num(pick(g, "rec", "Received Qty")), acc=num(pick(g, "acc", "Accepted Qty")), rej=num(pick(g, "rej", "Rejected Qty")), st=str(pick(g, "st", "Status", d="Pending QC")),
        grn=str(pick(g, "grn", "GRN No.")), by=str(pick(g, "by", "Inspected By")), notes=str(pick(g, "notes", "Notes")), lines=g.get("lines", []), src="canaresai"))
replace("gin", gin)
grn = []
for g in feed.get("grn", []):
    name = pick(g, "supplier", "Supplier")
    grn.append(dict(no=str(pick(g, "no", "GRN No.")), date=dt(pick(g, "date", "Date")), supName=name, sup=sup(pick(g, "supplier_code"), name), gin=str(pick(g, "gin", "GIN No.")),
        po=str(pick(g, "po", "PO No.")), qty=num(pick(g, "qty", "Accepted Qty")), by=str(pick(g, "by", "Inspected By")), lines=g.get("lines", []), src="canaresai"))
replace("grn", grn)
T["synced"] = datetime.now(timezone.utc).isoformat()
json.dump(T, open("transactions.json", "w"), separators=(",", ":"))
print(f"Synced {len(orders)} order lines, {len(gin)} GIN, {len(grn)} GRN")
