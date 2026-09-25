#!/usr/bin/env python3
"""Generate btp-lms-architecture.drawio — BTP E-Learning Platform architecture diagram set.

Source of truth for the .drawio artifact; run:  python3 tools/generate_drawio.py
Each page is a function below; pages without a function keep a placeholder frame.
Provider-neutral: infrastructure named by role, generic/hyperscaler-neutral icons only.
"""
import html

OUT = "/Users/arifistiak/code/beman/saas-lms/diagrams/btp-lms-architecture.drawio"

# ---------------------------------------------------------------- palette ---
ZONES = [
    ("Edge / Internet",          "#F8CECC", "#B85450"),
    ("DMZ",                      "#FFF2CC", "#D6B656"),
    ("Private App Subnet",       "#DAE8FC", "#6C8EBF"),
    ("Private Data Subnet",      "#D5E8D4", "#82B366"),
    ("Integration / Identity",   "#E1D5E7", "#9673A6"),
    ("External System",          "#F5F5F5", "#666666"),
]

SOLID   = "endArrow=classic;html=1;rounded=0;strokeWidth=1.5;fontSize=9;"
ASYNC   = "endArrow=classic;dashed=1;html=1;rounded=0;strokeWidth=1.5;fontSize=9;"
PENDING = "rounded=1;dashed=1;strokeColor=#999999;fontColor=#666666;fillColor=none;fontSize=10;"
NOTE    = "shape=note;size=14;align=left;spacing=8;fontSize=10;fillColor=#FFF9E6;strokeColor=#D6B656;"
ACTOR   = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fontSize=10;"
DB      = "shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=15;whiteSpace=wrap;html=1;fontSize=10;"

def esc(s): return html.escape(s, quote=True)

def box(id_, value, x, y, w, h, fill="#F5F5F5", stroke="#666666", style=""):
    st = f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=10;{style}"
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/></mxCell>'
            % (id_, esc(value), st, x, y, w, h))

def edge(id_, source, target, label="", style=SOLID, points=None):
    pts = ""
    if points:
        pts = "<Array as=\"points\">" + "".join("<mxPoint x=\"%d\" y=\"%d\"/>" % p for p in points) + "</Array>"
    return ('<mxCell id="%s" value="%s" style="%s" edge="1" parent="1" source="%s" target="%s">'
            '<mxGeometry relative="1" as="geometry">%s</mxGeometry></mxCell>' % (id_, esc(label), style, source, target, pts))

# ----------------------------------------------------------------- legend ---
def legend(lid):
    c = [f'<mxCell id="{lid}" value="Legend" style="swimlane;startSize=24;fontSize=11;fillColor=#FFFFFF;strokeColor=#666666;rounded=0;" vertex="1" parent="1"><mxGeometry x="880" y="80" width="360" height="350" as="geometry"/></mxCell>']
    y = 36
    for i, (name, fill, stroke) in enumerate(ZONES):
        c.append(f'<mxCell id="{lid}-z{i}" value="" style="rounded=1;fillColor={fill};strokeColor={stroke};" vertex="1" parent="{lid}"><mxGeometry x="10" y="{y}" width="24" height="16" as="geometry"/></mxCell>')
        c.append(f'<mxCell id="{lid}-zl{i}" value="{esc(name)}" style="text;fontSize=10;align=left;" vertex="1" parent="{lid}"><mxGeometry x="42" y="{y}" width="150" height="16" as="geometry"/></mxCell>')
        y += 22
    y += 6
    for i, (name, st) in enumerate([
        ("Sync flow", "endArrow=classic;html=1;rounded=0;strokeWidth=1.5;"),
        ("Async / background flow", "endArrow=classic;dashed=1;html=1;rounded=0;strokeWidth=1.5;"),
    ]):
        c.append(f'<mxCell id="{lid}-e{i}" style="{st}" edge="1" parent="{lid}"><mxGeometry relative="1" as="geometry"><mxPoint x="12" y="{y+8}" as="sourcePoint"/><mxPoint x="112" y="{y+8}" as="targetPoint"/></mxGeometry></mxCell>')
        c.append(f'<mxCell id="{lid}-el{i}" value="{esc(name)}" style="text;fontSize=10;align=left;" vertex="1" parent="{lid}"><mxGeometry x="122" y="{y}" width="220" height="16" as="geometry"/></mxCell>')
        y += 24
    c.append(f'<mxCell id="{lid}-pnd" value="Pending decision (ARCH-xx)" style="{PENDING}" vertex="1" parent="{lid}"><mxGeometry x="10" y="{y}" width="160" height="30" as="geometry"/></mxCell>')
    c.append(f'<mxCell id="{lid}-sec" value="Security control note" style="shape=note;size=10;fillColor=#FFF9E6;strokeColor=#D6B656;fontSize=10;" vertex="1" parent="{lid}"><mxGeometry x="190" y="{y}" width="150" height="30" as="geometry"/></mxCell>')
    y += 42
    c.append(f'<mxCell id="{lid}-stub" value="Entity stub → see page N" style="rounded=0;fillColor=#FFFFFF;strokeColor=#6C8EBF;fontSize=10;dashed=1;dashPattern=2 2;" vertex="1" parent="{lid}"><mxGeometry x="10" y="{y}" width="160" height="26" as="geometry"/></mxCell>')
    return c

# ------------------------------------------------------- page constructors ---
def page_frame(pid, title, srs):
    return [
        f'<mxCell id="{pid}-title" value="{esc(title)}" style="text;html=1;fontSize=20;fontStyle=1;align=left;" vertex="1" parent="1"><mxGeometry x="40" y="20" width="800" height="40" as="geometry"/></mxCell>',
        f'<mxCell id="{pid}-srs" value="Source: BTP-EL-SRS-001 {esc(srs)}" style="{NOTE}" vertex="1" parent="1"><mxGeometry x="40" y="770" width="240" height="36" as="geometry"/></mxCell>',
    ] + legend(f"{pid}-legend")

def placeholder(pid):
    return [f'<mxCell id="{pid}-ph" value="Content pending — implemented page-by-page (tasks 2.x–6.x)" style="rounded=1;dashed=1;strokeColor=#999999;fontColor=#999999;fontSize=13;fillColor=none;" vertex="1" parent="1"><mxGeometry x="240" y="340" width="520" height="110" as="geometry"/></mxCell>']

# --- page 1: system context ------------------------------------------------
def page_ctx():
    c = []
    c.append(box("ctx-sys",
        "<b>BTP E-Learning Platform</b><br><br>"
        "Public Portal &amp; Discovery · Authentication &amp; SSO · Course Master "
        "(bilingual versions) · Curriculum &amp; Content · Enrollment · Learner Dashboard · "
        "Assessment · Certification · Gamification · Notifications · Reporting · CMS · "
        "User Mgmt · Audit &amp; Operations",
        300, 200, 400, 260, fill="#DAE8FC", stroke="#6C8EBF", style="verticalAlign=middle;fontSize=10;"))
    c.append('<mxCell id="ctx-learner" value="%s" style="%s" vertex="1" parent="1"><mxGeometry x="80" y="210" width="50" height="70" as="geometry"/></mxCell>' % (esc("Learner /<br>Public User"), ACTOR))
    c.append('<mxCell id="ctx-admin" value="%s" style="%s" vertex="1" parent="1"><mxGeometry x="80" y="380" width="50" height="70" as="geometry"/></mxCell>' % (esc("Administrator"), ACTOR))
    c.append('<mxCell id="ctx-worker" value="%s" style="%s" vertex="1" parent="1"><mxGeometry x="80" y="560" width="50" height="70" as="geometry"/></mxCell>' % (esc("Background<br>Worker"), ACTOR))
    c.append(box("ctx-sso",  "<b>BTP SSO /</b><br><b>Identity Service</b><br><br>SSO login · profile sync · role mapping", 160, 600, 170, 90, fill="#E1D5E7", stroke="#9673A6"))
    c.append(box("ctx-gw",   "<b>Government Email / SMS Gateways</b><br><br>outbound notifications", 380, 600, 180, 90))
    c.append(box("ctx-pay",  "<b>Payment Provider</b><br><br><i>inactive — future extension (ARCH-pending)</i>", 610, 600, 170, 90, style=PENDING))
    c.append(box("ctx-siem", "<b>Monitoring / SIEM</b><br><br>logs · metrics · audit", 800, 600, 150, 90))
    c.append(box("ctx-dns",  "<b>Government DNS / Edge Protection</b><br><br>DDoS · WAF · TLS 1.2+", 300, 60, 400, 50, fill="#F8CECC", stroke="#B85450"))
    c.append(edge("ctx-e1", "ctx-learner", "ctx-sys", "HTTPS — browse / enroll / learn"))
    c.append(edge("ctx-e2", "ctx-admin", "ctx-sys", "administer — RBAC"))
    c.append(edge("ctx-e3", "ctx-sys", "ctx-worker", "enqueue jobs", ASYNC))
    c.append(edge("ctx-e4", "ctx-sys", "ctx-sso", "SSO redirect · profile sync"))
    c.append(edge("ctx-e5", "ctx-sys", "ctx-gw", "email / SMS (async)", ASYNC))
    c.append(edge("ctx-e6", "ctx-sys", "ctx-pay", "future extension (inactive)", ASYNC))
    c.append(edge("ctx-e7", "ctx-sys", "ctx-siem", "logs / metrics / audit"))
    c.append(edge("ctx-e8", "ctx-learner", "ctx-dns", "public HTTPS"))
    c.append(edge("ctx-e9", "ctx-dns", "ctx-sys", "filtered traffic"))
    return c

# --- page 2: logical component architecture -------------------------------
def svc(parent, id_, label, x, y, w=150, h=55, fill="#DAE8FC", stroke="#6C8EBF", style=""):
    c = box(f"{id_}", label, x, y, w, h, fill=fill, stroke=stroke,
            style="verticalAlign=middle;" + style)
    return c.replace('parent="1"', f'parent="{parent}"', 1)

def frame(id_, label, x, y, w, h, fill="#FFFFFF", stroke="#666666", parent="1"):
    return (f'<mxCell id="{id_}" value="{esc(label)}" style="swimlane;startSize=26;fontSize=11;'
            f'fillColor={fill};strokeColor={stroke};rounded=1;" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def page_comp():
    c = []
    # entry points
    c.append(box("comp-portal", "<b>Public Portal</b><br>catalogue · search · CMS pages", 40, 90, 230, 50, fill="#FFF2CC", stroke="#D6B656"))
    c.append(box("comp-admin", "<b>Admin Panel</b><br>RBAC permission sets — no instructor role (BR-007)", 310, 90, 250, 50, fill="#FFF2CC", stroke="#D6B656"))
    c.append(box("comp-cdn", "<b>CDN</b> — pending decision", 600, 90, 160, 50, style=PENDING))
    # application tier
    c.append(frame("comp-app", "Application Tier — App Servers (8 vCPU / 16 GB)", 40, 180, 820, 370, fill="#EEEEEE", stroke="#6C8EBF"))
    c.append(svc("comp-app", "comp-auth", "<b>Auth &amp; SSO Service</b><br>OTP · sessions · account linking", 15, 40, 160, 60))
    c.append(svc("comp-app", "comp-course", "<b>Course Master Service</b><br>Parent Course → Language Versions", 190, 35, 200, 62, fill="#FFE6CC", stroke="#D79B00", style="fontStyle=1"))
    c.append(svc("comp-app", "comp-vbn", "Version — Bangla", 190, 105, 95, 26, fill="#FFF2CC", stroke="#D79B00", style="fontSize=9;"))
    c.append(svc("comp-app", "comp-ven", "Version — English", 295, 105, 95, 26, fill="#FFF2CC", stroke="#D79B00", style="fontSize=9;"))
    c.append(svc("comp-app", "comp-br001", "1 parent → 1–2 versions · BR-001", 400, 105, 150, 26, style="fontSize=9;align=left;fillColor=none;strokeColor=none;fontColor=#D79B00;"))
    c.append(svc("comp-app", "comp-cur", "<b>Curriculum &amp; Content</b><br>modules · lessons · sequencing", 400, 40, 160, 60))
    c.append(svc("comp-app", "comp-media", "<b>Media Library</b><br>reuse · captions · transcripts", 575, 40, 140, 60))
    c.append(svc("comp-app", "comp-enr", "<b>Enrollment</b><br>self / admin / bulk · version-bound", 15, 150, 160, 60))
    c.append(svc("comp-app", "comp-prog", "<b>Progress &amp; Dashboard</b><br>resume · completion tracking", 190, 150, 200, 60))
    c.append(svc("comp-app", "comp-assess", "<b>Assessment</b><br>banks · quiz builder · grading", 400, 150, 160, 60))
    c.append(svc("comp-app", "comp-cert", "<b>Certification</b><br>templates · QR verify · PDF", 575, 150, 140, 60))
    c.append(svc("comp-app", "comp-gami", "<b>Gamification</b><br>restrained — optional features", 15, 260, 160, 60))
    c.append(svc("comp-app", "comp-notif", "<b>Notifications</b><br>templates per language", 190, 260, 200, 60))
    c.append(svc("comp-app", "comp-cms", "<b>CMS &amp; Config</b><br>pages · banners · feature flags", 400, 260, 160, 60))
    c.append(svc("comp-app", "comp-user", "<b>User Management</b><br>profiles · bulk import", 575, 260, 140, 60))
    c.append(svc("comp-app", "comp-rep", "<b>Reporting &amp; Analytics</b> — 12 reports incl. BN vs EN comparison", 15, 325, 330, 40))
    c.append(svc("comp-app", "comp-audit", "<b>Audit &amp; Operations</b> — trails · job monitors", 360, 325, 190, 40))
    # data tier
    c.append(frame("comp-data", "Data Tier — Private Data Subnet", 40, 590, 560, 130, fill="#D5E8D4", stroke="#82B366"))
    c.append(svc("comp-data", "comp-db", "Primary DB\n300–500 GB SSD", 15, 40, 100, 70, fill="#FFFFFF", stroke="#82B366", style=DB))
    c.append(svc("comp-data", "comp-repl", "Read Replica (optional)", 130, 40, 100, 70, fill="#FFFFFF", stroke="#82B366", style=DB))
    c.append(svc("comp-data", "comp-cache", "Cache (Redis-class)", 245, 50, 90, 55, fill="#FFFFFF", stroke="#82B366"))
    c.append(svc("comp-data", "comp-search", "Search Index (Solr-class)", 345, 50, 100, 55, fill="#FFFFFF", stroke="#82B366"))
    c.append(svc("comp-data", "comp-obj", "Object Storage 500 GB+", 455, 50, 90, 55, fill="#FFFFFF", stroke="#82B366"))
    # external stubs
    c.append(box("comp-sso", "<b>BTP SSO / Identity</b><br>(see page 1)", 640, 590, 170, 55, fill="#E1D5E7", stroke="#9673A6"))
    c.append(box("comp-gw", "<b>Gov Email / SMS Gateways</b><br>(see page 1)", 640, 665, 200, 50))
    # edges
    c.append(edge("comp-e1", "comp-portal", "comp-app", "HTTPS"))
    c.append(edge("comp-e2", "comp-admin", "comp-app", "admin API"))
    c.append(edge("comp-e3", "comp-app", "comp-data", "persist / query / cache"))
    c.append(edge("comp-e4", "comp-app", "comp-sso", "SSO · profile sync", SOLID + "exitX=0.68;exitY=1;entryX=0.5;entryY=0;"))
    c.append(edge("comp-e5", "comp-app", "comp-gw", "email / SMS (async)", ASYNC + "exitX=0.95;exitY=1;entryX=0.9;entryY=0;"))
    return c


# --- page 3: network / deployment ------------------------------------------
def page_net():
    c = []
    # edge zone
    c.append(frame("net-ze", "Internet / Edge Zone", 40, 70, 760, 95, fill="#F8CECC", stroke="#B85450"))
    c.append(svc("net-ze", "net-users", "Learners / Admins\n(public internet)", 15, 32, 120, 48, fill="#FFFFFF", stroke="#B85450", style="ellipse;shape=cloud;"))
    c.append(svc("net-ze", "net-dns", "Government DNS", 170, 36, 110, 40, fill="#FFFFFF", stroke="#B85450"))
    c.append(svc("net-ze", "net-waf", "DDoS Protection + WAF\nTLS 1.2+", 310, 30, 190, 50, fill="#FFFFFF", stroke="#B85450"))
    c.append(svc("net-ze", "net-cdn", "CDN\npending decision", 540, 30, 130, 50, style=PENDING))
    # dmz
    c.append(frame("net-zd", "DMZ — reverse proxies & API gateway only", 40, 185, 760, 95, fill="#FFF2CC", stroke="#D6B656"))
    c.append(svc("net-zd", "net-lb1", "Load Balancer 1", 15, 36, 110, 42, fill="#FFFFFF", stroke="#D6B656"))
    c.append(svc("net-zd", "net-lb2", "Load Balancer 2", 140, 36, 110, 42, fill="#FFFFFF", stroke="#D6B656"))
    c.append(svc("net-zd", "net-gw", "Reverse Proxy / API Gateway", 290, 36, 180, 42, fill="#FFFFFF", stroke="#D6B656"))
    c.append(svc("net-zd", "net-mfa", "MFA for privileged accounts · admin access via jump host", 500, 30, 240, 50, style=NOTE))
    # app subnet
    c.append(frame("net-za", "Private Application Subnet", 40, 300, 760, 95, fill="#DAE8FC", stroke="#6C8EBF"))
    c.append(svc("net-za", "net-app1", "App Server 1 (8 vCPU / 16 GB)", 15, 36, 150, 42, fill="#FFFFFF", stroke="#6C8EBF"))
    c.append(svc("net-za", "net-app2", "App Server 2 (8 vCPU / 16 GB)", 180, 36, 150, 42, fill="#FFFFFF", stroke="#6C8EBF"))
    c.append(svc("net-za", "net-wrk", "Background Workers ×1–2\n(certificates · notifications · reports)", 350, 30, 220, 50, fill="#FFFFFF", stroke="#6C8EBF"))
    c.append(svc("net-za", "net-rbac", "RBAC least-privilege · secrets management", 600, 30, 145, 50, style=NOTE))
    # data subnet
    c.append(frame("net-zf", "Private Data Subnet", 40, 415, 760, 115, fill="#D5E8D4", stroke="#82B366"))
    c.append(svc("net-zf", "net-db", "Primary DB\n8 vCPU / 16–32 GB\n300–500 GB SSD", 15, 32, 110, 70, fill="#FFFFFF", stroke="#82B366", style=DB))
    c.append(svc("net-zf", "net-repl", "Read Replica (optional)", 140, 32, 100, 70, fill="#FFFFFF", stroke="#82B366", style=DB))
    c.append(svc("net-zf", "net-cache", "Cache (Redis-class)", 255, 42, 95, 50, fill="#FFFFFF", stroke="#82B366"))
    c.append(svc("net-zf", "net-srch", "Search (Solr-class)", 360, 42, 90, 50, fill="#FFFFFF", stroke="#82B366"))
    c.append(svc("net-zf", "net-obj", "Object Storage 500 GB+", 460, 42, 105, 50, fill="#FFFFFF", stroke="#82B366"))
    c.append(svc("net-zf", "net-enc", "Encryption at rest · daily backups + PITR · restore testing", 580, 36, 165, 60, style=NOTE))
    # integration layer
    c.append(frame("net-zi", "Integration / Identity Layer", 40, 550, 760, 80, fill="#E1D5E7", stroke="#9673A6"))
    c.append(svc("net-zi", "net-sso", "BTP SSO / Identity Service", 15, 28, 170, 40, fill="#FFFFFF", stroke="#9673A6"))
    c.append(svc("net-zi", "net-gw2", "Gov Email / SMS Gateways", 200, 28, 170, 40, fill="#FFFFFF", stroke="#9673A6"))
    c.append(svc("net-zi", "net-pay", "Payment (inactive — future)", 385, 28, 170, 40, style=PENDING))
    # monitoring + env inset
    c.append(frame("net-mon", "Monitoring Node + SIEM", 40, 650, 360, 80, fill="#F5F5F5", stroke="#666666"))
    c.append(svc("net-mon", "net-metr", "Metrics / Alerts", 15, 32, 100, 34, fill="#FFFFFF", stroke="#666666"))
    c.append(svc("net-mon", "net-logs", "Central Logs", 125, 32, 100, 34, fill="#FFFFFF", stroke="#666666"))
    c.append(svc("net-mon", "net-audit", "SIEM / Audit", 235, 32, 100, 34, fill="#FFFFFF", stroke="#666666"))
    c.append(frame("net-env", "Environments & Promotion", 430, 650, 370, 80, fill="#FFFFFF", stroke="#666666"))
    c.append(svc("net-env", "net-e1", "Dev", 12, 36, 52, 30, fill="#FFFFFF", stroke="#666666"))
    c.append(svc("net-env", "net-e2", "Staging", 76, 36, 56, 30, fill="#FFFFFF", stroke="#666666"))
    c.append(svc("net-env", "net-e3", "UAT", 144, 36, 52, 30, fill="#FFFFFF", stroke="#666666"))
    c.append(svc("net-env", "net-e4", "Prod", 208, 36, 52, 30, fill="#FFFFFF", stroke="#666666"))
    c.append(svc("net-env", "net-e5", "DR — RPO/RTO pending NDC/BCC", 272, 30, 88, 42, style=PENDING))
    for a, b in (("net-e1", "net-e2"), ("net-e2", "net-e3"), ("net-e3", "net-e4"), ("net-e4", "net-e5")):
        c.append(edge("net-ee-" + a, a, b, style="endArrow=classic;html=1;rounded=0;strokeWidth=1;fontSize=8;"))
    # zone-to-zone traffic
    c.append(edge("net-t1", "net-ze", "net-zd", "443 · deny-by-default firewall between zones", SOLID + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"))
    c.append(edge("net-t2", "net-zd", "net-za", "app traffic", SOLID + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"))
    c.append(edge("net-t3", "net-za", "net-zf", "SQL / cache / object I/O", SOLID + "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"))
    c.append(edge("net-t4", "net-za", "net-zi", "egress: SSO · notifications", SOLID + "exitX=1;exitY=0.5;entryX=1;entryY=0.5;", points=[(838, 347), (838, 590)]))
    c.append(edge("net-t5", "net-za", "net-mon", "logs / metrics / audit", ASYNC + "exitX=0;exitY=0.5;entryX=0;entryY=0.4;", points=[(26, 347), (26, 682)]))
    c.append(edge("net-t6", "net-zf", "net-mon", "backup verification", ASYNC + "exitX=0;exitY=0.5;entryX=0;entryY=0.8;", points=[(14, 472), (14, 714)]))
    # managed-category note (task 3.4)
    c.append(box("net-map", "<i>Generic blocks map to managed-service categories: managed load balancing · managed relational DB (+replica) · managed cache / search / object storage · managed monitoring. Provider-neutral by design — hosting location &amp; HA model are open decisions (ARCH).</i>", 40, 742, 760, 34, style="fillColor=none;strokeColor=none;align=left;fontSize=9;fontColor=#666666;"))
    return c


# --- ERD helpers ------------------------------------------------------------
def entity(id_, name, attrs, x, y, w, h, dashed=False):
    body = "<b>%s</b><br><font style='font-size:8px'>%s</font>" % (name, "<br>".join(attrs))
    st = "rounded=0;whiteSpace=wrap;html=1;align=left;spacing=6;spacingTop=2;fontSize=10;verticalAlign=top;fillColor=#DAE8FC;strokeColor=#6C8EBF;"
    if dashed:
        st += "dashed=1;dashPattern=2 2;"
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/></mxCell>'
            % (id_, esc(body), st, x, y, w, h))

def rel(id_, a, b, label, style="", points=None):
    return edge(id_, a, b, label, "endArrow=none;html=1;rounded=0;strokeWidth=1;fontSize=9;fontStyle=1;" + style, points)

def page_erd1():
    c = []
    c.append(entity("e1-parent", "PARENT_COURSE", ["«PK» course_id", "title · slug · category", "created_by · status"], 40, 80, 180, 84))
    c.append(entity("e1-ver", "COURSE_LANGUAGE_VERSION", ["«PK» version_id", "«FK» parent_course_id", "language (BN | EN)", "status: draft→published→archived", "access_rule · window · capacity"], 40, 215, 200, 110))
    c.append(entity("e1-mod", "MODULE", ["«PK» module_id", "«FK» version_id", "title · sequence"], 40, 380, 160, 74))
    c.append(entity("e1-les", "LESSON", ["«PK» lesson_id", "«FK» module_id", "type: video|html|pdf|", "interactive|external", "content_ref · completion_rule"], 40, 505, 180, 96))
    c.append(entity("e1-med", "MEDIA_RESOURCE", ["«PK» media_id", "«FK» version_id", "type · url · captions_ref"], 40, 650, 180, 74))
    c.append(entity("e1-bank", "QUESTION_BANK", ["«PK» bank_id", "«FK» version_id"], 310, 80, 160, 64))
    c.append(entity("e1-q", "QUESTION", ["«PK» question_id", "«FK» bank_id", "type: MCQ|multi|TF|short|", "matching|descriptive", "options · answer_key"], 310, 195, 170, 96))
    c.append(entity("e1-as", "ASSESSMENT", ["«PK» assessment_id", "«FK» version_id", "attempts · time_limit", "randomization · pass_score", "manual_grading"], 310, 340, 190, 100))
    c.append(entity("e1-att", "ATTEMPT", ["«PK» attempt_id", "«FK» assessment_id · «FK» user_id", "started_at · submitted_at", "score · outcome"], 310, 495, 200, 90))
    c.append(entity("e1-ans", "ANSWER", ["«PK» answer_id", "«FK» attempt_id · «FK» question_id", "response · is_correct"], 310, 635, 200, 74))
    c.append(entity("e1-user", "USER (learner) → page 5", ["entity stub — see ERD platform page"], 580, 80, 210, 40, dashed=True))
    c.append(entity("e1-enr", "ENROLLMENT", ["«PK» enrollment_id", "«FK» user_id · «FK» version_id", "status · enrolled_at", "source: self|admin|bulk"], 580, 170, 200, 100))
    c.append(entity("e1-prog", "PROGRESS_RECORD", ["«PK» progress_id", "«FK» enrollment_id", "«FK» lesson_id", "completed_at · score"], 580, 330, 190, 90))
    c.append(entity("e1-cert", "CERTIFICATE", ["«PK» cert_id (unique ID)", "«FK» template_id · «FK» enrollment_id", "issued_at · qr_code", "status: active|revoked|reissued"], 580, 475, 210, 96))
    c.append(entity("e1-tpl", "CERTIFICATE_TEMPLATE", ["«PK» template_id", "language layout", "logo · signature · QR config"], 580, 625, 200, 84))
    c.append(rel("e1-r1", "e1-parent", "e1-ver", "1 — 0..2 (BN/EN, extensible)"))
    c.append(rel("e1-r2", "e1-ver", "e1-mod", "1 — N"))
    c.append(rel("e1-r3", "e1-mod", "e1-les", "1 — N"))
    c.append(rel("e1-r4", "e1-ver", "e1-med", "1 — N", points=[(255, 300), (255, 687)], ))
    c.append(rel("e1-r5", "e1-ver", "e1-bank", "1 — N", points=[(240, 240), (285, 240), (285, 112)], style="exitX=0;exitY=0.5;entryX=0;entryY=0.5;"))
    c.append(rel("e1-r6", "e1-bank", "e1-q", "1 — N"))
    c.append(rel("e1-r7", "e1-ver", "e1-as", "1 — N", points=[(250, 300), (270, 300), (270, 390)], style="exitX=0;exitY=0.75;entryX=0;entryY=0.5;"))
    c.append(rel("e1-r8", "e1-as", "e1-bank", "draws (randomized)", style="dashed=1;endArrow=open;endFill=0;exitX=1;exitY=0.3;entryX=0.5;entryY=0;", points=[(545, 370), (545, 62), (390, 62)]))
    c.append(rel("e1-r9", "e1-as", "e1-att", "1 — N"))
    c.append(rel("e1-r10", "e1-att", "e1-ans", "1 — N"))
    c.append(rel("e1-r11", "e1-ans", "e1-q", "N — 1", points=[(540, 672), (540, 243)], style="exitX=1;exitY=0.5;entryX=1;entryY=0.5;"))
    c.append(rel("e1-r12", "e1-user", "e1-enr", "1 (learner) — N"))
    c.append(rel("e1-r13", "e1-ver", "e1-enr", "1 — N", points=[(190, 168), (620, 168)], style="exitX=0.75;exitY=0;entryX=0.2;entryY=0;"))
    c.append(rel("e1-r14", "e1-enr", "e1-prog", "1 — N"))
    c.append(rel("e1-r15", "e1-prog", "e1-les", "N — 1", points=[(580, 375), (265, 375), (265, 480), (130, 480)], style="exitX=0;exitY=0.5;entryX=0.5;entryY=0;"))
    c.append(rel("e1-r16", "e1-enr", "e1-cert", "1 — 0..1"))
    c.append(rel("e1-r17", "e1-tpl", "e1-cert", "1 — N"))
    return c


# --- page 5: ERD platform & audit domain ------------------------------------
def page_erd2():
    c = []
    c.append(entity("e2-user", "USER", ["«PK» user_id", "btp_sso_id (nullable)", "email (verified) · phone", "password_hash (direct login)", "status: pending|active|suspended|deletion_requested", "consent · created_at"], 40, 90, 250, 130))
    c.append(entity("e2-prof", "LEARNER_PROFILE", ["«PK» profile_id · «FK» user_id", "name (BN / EN) · photo", "organisation · designation", "language_preference"], 40, 280, 230, 100))
    c.append(entity("e2-admin", "ADMIN_ROLE (permission set)", ["«PK» admin_role_id · «FK» user_id", "permissions: view|create|edit|publish|", "delete|approve|export|configure", "«super admin = permission set, not a role»"], 40, 440, 250, 110))
    c.append(entity("e2-login", "LOGIN_AUDIT", ["«PK» login_id · «FK» user_id", "at · ip · method: sso|direct", "outcome: success|failed"], 40, 610, 230, 90))
    c.append(entity("e2-not", "NOTIFICATION", ["«PK» notification_id · «FK» user_id", "event_type · language", "channel: email|sms · status"], 360, 90, 210, 100))
    c.append(entity("e2-dlog", "DELIVERY_LOG", ["«PK» log_id · «FK» notification_id", "gateway_ref · sent_at", "status: sent|failed|retried"], 360, 260, 210, 90))
    c.append(entity("e2-audit", "AUDIT_LOG", ["«PK» audit_id · actor_id", "entity · action", "before_value · after_value", "at · ip · session_ref"], 360, 430, 210, 110))
    c.append(entity("e2-cfg", "CONFIG_HISTORY", ["«PK» config_id", "«FK» setting_key", "old_value · new_value", "changed_by · at"], 360, 610, 200, 100))
    c.append(entity("e2-cat", "CATEGORY (taxonomy)", ["«PK» category_id", "name (BN / EN)", "«FK» parent_category_id (tree)"], 640, 90, 190, 90))
    c.append(entity("e2-tag", "TAG", ["«PK» tag_id · name", "applies to course versions"], 640, 240, 190, 70))
    c.append(entity("e2-imp", "INTEGRATION_MAPPING", ["«PK» mapping_id", "external_system · external_id", "internal_entity · internal_id", "idempotency_key · last_sync_at"], 640, 370, 220, 110))
    c.append(entity("e2-set", "SYSTEM_SETTING", ["«PK» setting_key", "value · scope", "feature_flag (on/off)"], 640, 540, 190, 90))
    c.append(entity("e2-stub", "COURSE_LANGUAGE_VERSION → page 4", ["entity stub — tagging target"], 640, 690, 220, 40, dashed=True))
    c.append(rel("e2-r1", "e2-user", "e2-prof", "1 — 1"))
    c.append(rel("e2-r2", "e2-user", "e2-not", "1 — N"))
    c.append(rel("e2-r3", "e2-not", "e2-dlog", "1 — N"))
    c.append(rel("e2-r4", "e2-user", "e2-admin", "1 — 0..1 (privileged)"))
    c.append(rel("e2-r5", "e2-user", "e2-login", "1 — N", points=[(22, 155), (22, 655)], style="exitX=0;exitY=0.5;entryX=0;entryY=0.5;"))
    c.append(rel("e2-r6", "e2-user", "e2-audit", "1 — N (as actor)", points=[(290, 200), (320, 200), (320, 470)], style="exitX=1;exitY=0.8;entryX=0;entryY=0.35;"))
    c.append(rel("e2-r7", "e2-admin", "e2-audit", "creates entries", style="dashed=1;endArrow=open;endFill=0;"))
    c.append(rel("e2-r8", "e2-set", "e2-cfg", "changes recorded in", style="dashed=1;endArrow=open;endFill=0;exitX=0;exitY=0.5;entryX=1;entryY=0.3;", points=[(600, 585), (600, 640)]))
    c.append(rel("e2-r9", "e2-cat", "e2-cat", "parent (self)", style="dashed=1;endArrow=open;endFill=0;exitX=0;exitY=0.25;entryX=0;entryY=0.75;", points=[(615, 112), (615, 157)]))
    c.append(rel("e2-r10", "e2-tag", "e2-stub", "N — M (tagging)", style="dashed=1;endArrow=open;endFill=0;"))
    return c

# --- page 6: state / lifecycle ----------------------------------------------
def state_node(id_, label, x, y, w=130, h=44, fill="#DAE8FC", stroke="#6C8EBF"):
    return box(id_, label, x, y, w, h, fill=fill, stroke=stroke, style="rounded=1;arcSize=40;whiteSpace=wrap;fontSize=10;")

def start_dot(id_, x, y):
    return ('<mxCell id="%s" value="" style="ellipse;fillColor=#000000;strokeColor=#000000;" vertex="1" parent="1">'
            '<mxGeometry x="%d" y="%d" width="20" height="20" as="geometry"/></mxCell>' % (id_, x, y))

def page_state():
    c = []
    c.append(box("st-note", "<i>Statuses per SRS §5.3–5.6. Enrollment language-switch policy and completion rules are pending client approval (AP items).</i>", 40, 60, 620, 30, style="fillColor=none;strokeColor=none;align=left;fontSize=10;fontColor=#666666;"))
    # lane 1 — course language version
    c.append(box("st-l1", "<b>Course Language Version</b>", 40, 120, 160, 30, style="fillColor=none;strokeColor=none;align=left;fontSize=12;"))
    c.append(start_dot("st-l1s", 230, 152))
    c.append(state_node("st-draft", "Draft", 290, 140, 120, 44, fill="#F5F5F5", stroke="#999999"))
    c.append(state_node("st-pub", "Published", 480, 140, 120, 44, fill="#D5E8D4", stroke="#82B366"))
    c.append(state_node("st-arch", "Archived", 670, 140, 120, 44, fill="#FFE6CC", stroke="#D79B00"))
    c.append(edge("st-e1", "st-l1s", "st-draft", "create", style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;"))
    c.append(edge("st-e2", "st-draft", "st-pub", "publish (admin)", style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;"))
    c.append(edge("st-e3", "st-pub", "st-arch", "archive", style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;"))
    c.append(edge("st-e4", "st-pub", "st-draft", "unpublish / return", style="endArrow=classic;dashed=1;html=1;strokeWidth=1.5;fontSize=9;exitX=0.25;exitY=1;entryX=0.25;entryY=1;", points=[(510, 215), (350, 215)]))
    # lane 2 — enrollment
    c.append(box("st-l2", "<b>Enrollment</b>", 40, 280, 160, 30, style="fillColor=none;strokeColor=none;align=left;fontSize=12;"))
    c.append(start_dot("st-l2s", 230, 312))
    c.append(state_node("st-act", "Active", 290, 300, 120, 44))
    c.append(state_node("st-comp", "Completed", 510, 270, 130, 44, fill="#D5E8D4", stroke="#82B366"))
    c.append(state_node("st-with", "Withdrawn", 510, 360, 130, 44, fill="#F8CECC", stroke="#B85450"))
    c.append(edge("st-e5", "st-l2s", "st-act", "enroll (version-bound)", style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;"))
    c.append(edge("st-e6", "st-act", "st-comp", "all modules complete", style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;"))
    c.append(edge("st-e7", "st-act", "st-with", "drop / admin remove", style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;"))
    c.append(edge("st-e8", "st-with", "st-act", "re-enroll", style="endArrow=classic;dashed=1;html=1;strokeWidth=1.5;fontSize=9;exitX=0;exitY=0.75;entryX=0;entryY=0.75;", points=[(465, 393), (465, 333)]))
    # lane 3 — account
    c.append(box("st-l3", "<b>User Account</b>", 40, 470, 160, 30, style="fillColor=none;strokeColor=none;align=left;fontSize=12;"))
    c.append(start_dot("st-l3s", 230, 502))
    c.append(state_node("st-pend", "Pending Verification (OTP)", 270, 490, 170, 44, fill="#FFF2CC", stroke="#D6B656"))
    c.append(state_node("st-aact", "Active", 510, 490, 110, 44))
    c.append(state_node("st-susp", "Suspended", 680, 490, 120, 44, fill="#F8CECC", stroke="#B85450"))
    c.append(state_node("st-del", "Deletion Requested → purged per retention policy", 480, 590, 250, 50, fill="#F5F5F5", stroke="#999999"))
    c.append(edge("st-e9", "st-l3s", "st-pend", "register", style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;"))
    c.append(edge("st-e10", "st-pend", "st-aact", "verify OTP / SSO link", style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;"))
    c.append(edge("st-e11", "st-aact", "st-susp", "violation / admin", style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;"))
    c.append(edge("st-e12", "st-susp", "st-aact", "reinstate", style="endArrow=classic;dashed=1;html=1;strokeWidth=1.5;fontSize=9;exitX=0.25;exitY=1;entryX=0.75;entryY=1;", points=[(710, 560), (590, 560)]))
    c.append(edge("st-e13", "st-aact", "st-del", "GDPR-style request", style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;exitX=0.5;exitY=1;entryX=0.5;entryY=0;"))
    return c

# --- sequence helpers --------------------------------------------------------
def seq_participant(id_, label, cx, fill="#DAE8FC", stroke="#6C8EBF", actor=False):
    w = 60 if actor else 130
    st = ACTOR if actor else "rounded=1;whiteSpace=wrap;html=1;fontSize=10;fontStyle=1;"
    return ('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
            '<mxGeometry x="%d" y="85" width="%d" height="44" as="geometry"/></mxCell>'
            % (id_, esc(label), st, cx - w // 2, w)) if not actor else (
        '<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
        '<mxGeometry x="%d" y="80" width="%d" height="56" as="geometry"/></mxCell>'
        % (id_, esc(label), st, cx - w // 2, w))

def seq_lifeline(id_, anchor, cx, y2=730):
    return ('<mxCell id="%s" style="endArrow=none;dashed=1;html=1;strokeColor=#999999;" edge="1" parent="1" source="%s">'
            '<mxGeometry relative="1" as="geometry"><mxPoint x="%d" y="730" as="targetPoint"/></mxGeometry></mxCell>'
            % (id_, anchor, cx))

def seq_msg(id_, a, b, label, y, ay, by, dashed=False):
    st = ("endArrow=classic;dashed=1;html=1;strokeWidth=1.5;fontSize=9;" if dashed
          else "endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;")
    return ('<mxCell id="%s" value="%s" style="%s" edge="1" parent="1">'
            '<mxGeometry relative="1" as="geometry">'
            '<mxPoint x="%d" y="%d" as="sourcePoint"/><mxPoint x="%d" y="%d" as="targetPoint"/>'
            '</mxGeometry></mxCell>' % (id_, esc(label), st, a, y, b, y))

def seq_self(id_, x, label, y):
    return ('<mxCell id="%s" value="%s" style="endArrow=classic;html=1;strokeWidth=1.5;fontSize=9;align=left;spacingLeft=4;" edge="1" parent="1">'
            '<mxGeometry relative="1" as="geometry">'
            '<mxPoint x="%d" y="%d" as="sourcePoint"/><mxPoint x="%d" y="%d" as="targetPoint"/>'
            '<Array as="points"><mxPoint x="%d" y="%d"/><mxPoint x="%d" y="%d"/></Array>'
            '</mxGeometry></mxCell>' % (id_, esc(label), x, y, x + 10, y + 34, x + 90, y, x + 90, y + 34))

def seq_section(id_, label, y):
    return ('<mxCell id="%s" value="%s" style="text;html=1;fontSize=11;fontStyle=5;fontColor=#6C8EBF;align=left;" vertex="1" parent="1">'
            '<mxGeometry x="50" y="%d" width="700" height="20" as="geometry"/></mxCell>' % (id_, esc(label), y))

# --- page 7: sequence auth & sso ---------------------------------------------
def page_seq1():
    c = []
    X = {"learner": 100, "portal": 270, "auth": 450, "btp": 630, "gw": 790}
    c.append(seq_participant("s1-learner", "Learner", X["learner"], actor=True))
    c.append(seq_participant("s1-portal", "Public Portal", X["portal"]))
    c.append(seq_participant("s1-auth", "Auth &amp; SSO Service", X["auth"], fill="#FFE6CC", stroke="#D79B00"))
    c.append(seq_participant("s1-btp", "BTP SSO / Identity", X["btp"], fill="#E1D5E7", stroke="#9673A6"))
    c.append(seq_participant("s1-gw", "Email/SMS Gateway", X["gw"], fill="#F5F5F5", stroke="#666666"))
    for k, v in X.items():
        c.append(seq_lifeline("s1-ll-" + k, "s1-" + k, v))
    y = 130
    c.append(seq_section("s1-secA", "A · SSO login (protocol pending decision — ARCH)", y)); y += 30
    c.append(seq_msg("s1-m1", X["learner"], X["portal"], "1 · login with BTP SSO", y, X["learner"], X["portal"])); y += 25
    c.append(seq_msg("s1-m2", X["portal"], X["auth"], "2 · initiate SSO", y, X["portal"], X["auth"])); y += 25
    c.append(seq_msg("s1-m3", X["auth"], X["btp"], "3 · redirect to BTP SSO", y, X["auth"], X["btp"])); y += 25
    c.append(seq_self("s1-m4", X["btp"], "4 · authenticate at identity provider", y)); y += 48
    c.append(seq_msg("s1-m5", X["btp"], X["auth"], "5 · assertion / token + profile", y, X["btp"], X["auth"])); y += 25
    c.append(seq_self("s1-m6", X["auth"], "6 · map role · create/link session · audit log", y)); y += 48
    c.append(seq_msg("s1-m7", X["auth"], X["learner"], "7 · logged in", y, X["auth"], X["learner"])); y += 45
    c.append(seq_section("s1-secB", "B · Self-registration with OTP verification", y)); y += 30
    c.append(seq_msg("s1-m8", X["learner"], X["portal"], "8 · register (email / phone)", y, X["learner"], X["portal"])); y += 25
    c.append(seq_msg("s1-m9", X["portal"], X["auth"], "9 · create pending account", y, X["portal"], X["auth"])); y += 25
    c.append(seq_msg("s1-m10", X["auth"], X["gw"], "10 · send OTP", y, X["auth"], X["gw"], dashed=True)); y += 25
    c.append(seq_msg("s1-m11", X["gw"], X["learner"], "11 · OTP received", y, X["gw"], X["learner"], dashed=True)); y += 25
    c.append(seq_msg("s1-m12", X["learner"], X["auth"], "12 · submit OTP", y, X["learner"], X["auth"])); y += 25
    c.append(seq_msg("s1-m13", X["auth"], X["learner"], "13 · account Active", y, X["auth"], X["learner"])); y += 45
    c.append(seq_section("s1-secC", "C · Account linking (SSO ↔ existing account)", y)); y += 30
    c.append(seq_msg("s1-m14", X["learner"], X["auth"], "14 · request link", y, X["learner"], X["auth"])); y += 25
    c.append(seq_msg("s1-m15", X["auth"], X["btp"], "15 · verify identity match", y, X["auth"], X["btp"])); y += 25
    c.append(seq_self("s1-m16", X["auth"], "16 · store btp_sso_id (audit logged)", y))
    return c

# --- page 8: sequence learning lifecycle -------------------------------------
def page_seq2():
    c = []
    X = {"learner": 95, "portal": 235, "enr": 395, "asmt": 545, "cert": 690, "wrk": 815}
    c.append(seq_participant("s2-learner", "Learner", X["learner"], actor=True))
    c.append(seq_participant("s2-portal", "Portal / Player", X["portal"]))
    c.append(seq_participant("s2-enr", "Enrollment & Progress", X["enr"], fill="#FFE6CC", stroke="#D79B00"))
    c.append(seq_participant("s2-asmt", "Assessment", X["asmt"]))
    c.append(seq_participant("s2-cert", "Certification", X["cert"]))
    c.append(seq_participant("s2-wrk", "Worker", X["wrk"], fill="#F5F5F5", stroke="#666666"))
    for k, v in X.items():
        c.append(seq_lifeline("s2-ll-" + k, "s2-" + k, v))
    y = 125
    c.append(seq_section("s2-secA", "A · Discover & enroll (per language version)", y)); y += 28
    c.append(seq_msg("s2-m1", X["learner"], X["portal"], "1 · browse catalogue (BN / EN)", y, X["learner"], X["portal"])); y += 24
    c.append(seq_msg("s2-m2", X["learner"], X["enr"], "2 · self-enroll", y, X["learner"], X["enr"])); y += 24
    c.append(seq_self("s2-m3", X["enr"], "3 · duplicate · window · capacity checks", y)); y += 46
    c.append(seq_msg("s2-m4", X["enr"], X["learner"], "4 · enrolled — Active (version-bound)", y, X["enr"], X["learner"])); y += 40
    c.append(seq_section("s2-secB", "B · Learn & progress", y)); y += 28
    c.append(seq_msg("s2-m5", X["learner"], X["portal"], "5 · open / resume lesson", y, X["learner"], X["portal"])); y += 24
    c.append(seq_msg("s2-m6", X["portal"], X["enr"], "6 · progress events (completion rules)", y, X["portal"], X["enr"])); y += 24
    c.append(seq_self("s2-m7", X["enr"], "7 · update module % · history", y)); y += 46
    c.append(seq_section("s2-secC", "C · Assessment", y)); y += 28
    c.append(seq_msg("s2-m8", X["learner"], X["asmt"], "8 · start attempt (randomized, timed)", y, X["learner"], X["asmt"])); y += 24
    c.append(seq_self("s2-m9", X["asmt"], "9 · auto-grade · manual grading queue", y)); y += 46
    c.append(seq_msg("s2-m10", X["asmt"], X["enr"], "10 · pass → module completion", y, X["asmt"], X["enr"])); y += 40
    c.append(seq_section("s2-secD", "D · Completion & certification (async)", y)); y += 28
    c.append(seq_self("s2-m11", X["enr"], "11 · all modules complete → Completed", y)); y += 46
    c.append(seq_msg("s2-m12", X["enr"], X["wrk"], "12 · enqueue certificate job", y, X["enr"], X["wrk"], dashed=True)); y += 24
    c.append(seq_msg("s2-m13", X["wrk"], X["cert"], "13 · render PDF from template + QR", y, X["wrk"], X["cert"], dashed=True)); y += 24
    c.append(seq_msg("s2-m14", X["cert"], X["learner"], "14 · certificate issued (unique ID) + notification", y, X["cert"], X["learner"], dashed=True))
    return c

# --- page 9: sequence content publishing -------------------------------------
def page_seq3():
    c = []
    X = {"admin": 100, "panel": 260, "course": 440, "media": 610, "portal": 770}
    c.append(seq_participant("s3-admin", "Administrator", X["admin"], actor=True))
    c.append(seq_participant("s3-panel", "Admin Panel", X["panel"]))
    c.append(seq_participant("s3-course", "Course Master Service", X["course"], fill="#FFE6CC", stroke="#D79B00"))
    c.append(seq_participant("s3-media", "Media Library", X["media"]))
    c.append(seq_participant("s3-portal", "Public Portal", X["portal"], fill="#FFF2CC", stroke="#D6B656"))
    for k, v in X.items():
        c.append(seq_lifeline("s3-ll-" + k, "s3-" + k, v))
    y = 130
    c.append(seq_section("s3-secA", "A · Create parent course + language versions (BR-001: create once, never duplicate)", y)); y += 30
    c.append(seq_msg("s3-m1", X["admin"], X["panel"], "1 · create parent course", y, X["admin"], X["panel"])); y += 25
    c.append(seq_msg("s3-m2", X["panel"], X["course"], "2 · create PARENT_COURSE", y, X["panel"], X["course"])); y += 25
    c.append(seq_msg("s3-m3", X["admin"], X["panel"], "3 · create Bangla + English versions", y, X["admin"], X["panel"])); y += 25
    c.append(seq_msg("s3-m4", X["panel"], X["course"], "4 · create versions (independent statuses)", y, X["panel"], X["course"])); y += 30
    c.append(seq_section("s3-secB", "B · Build curriculum", y)); y += 30
    c.append(seq_msg("s3-m5", X["admin"], X["course"], "5 · add modules / lessons (per version)", y, X["admin"], X["course"])); y += 25
    c.append(seq_msg("s3-m6", X["course"], X["media"], "6 · attach media (library reuse, captions)", y, X["course"], X["media"])); y += 25
    c.append(seq_msg("s3-m7", X["admin"], X["course"], "7 · set completion rules · previews · access rules", y, X["admin"], X["course"])); y += 30
    c.append(seq_section("s3-secC", "C · Publish & maintain", y)); y += 30
    c.append(seq_msg("s3-m8", X["admin"], X["course"], "8 · publish version (Draft → Published)", y, X["admin"], X["course"])); y += 25
    c.append(seq_msg("s3-m9", X["course"], X["portal"], "9 · appears in catalogue per access rules", y, X["course"], X["portal"])); y += 25
    c.append(seq_msg("s3-m10", X["admin"], X["course"], "10 · update (draft edit) / unpublish / archive", y, X["admin"], X["course"], dashed=True))
    return c

# --- page 10: integration, observability, backup & DR -------------------------
def page_ops():
    c = []
    c.append(box("op-h1", "<b>Integration &amp; Async Processing</b>", 40, 75, 400, 26, style="fillColor=none;strokeColor=none;align=left;fontSize=13;"))
    c.append(box("op-app", "<b>Application Tier</b>", 80, 115, 180, 60, fill="#DAE8FC", stroke="#6C8EBF"))
    c.append(box("op-gw", "<b>BTP API Gateway</b><br>role mapping · error handling", 460, 115, 200, 60, fill="#E1D5E7", stroke="#9673A6"))
    c.append(box("op-q", "<b>Job Queue</b><br>retry with backoff · idempotency keys", 80, 235, 220, 60, fill="#FFF2CC", stroke="#D6B656"))
    c.append(box("op-wrk", "<b>Background Workers</b><br>certificates · notifications · reports", 460, 235, 200, 60))
    c.append(box("op-sms", "<b>Gov Email / SMS Gateways</b>", 80, 355, 220, 55, fill="#F5F5F5", stroke="#666666"))
    c.append(box("op-log", "<b>Delivery Log</b><br>sent | failed | retried", 460, 355, 200, 55, fill="#D5E8D4", stroke="#82B366"))
    c.append(box("op-dl", "<i>failed sends → retry → dead-letter (monitored)</i>", 320, 425, 340, 24, style="fillColor=none;strokeColor=none;align=left;fontSize=9;fontColor=#666666;"))
    c.append(edge("op-e1", "op-app", "op-gw", "sync · profile sync"))
    c.append(edge("op-e2", "op-app", "op-q", "enqueue"))
    c.append(edge("op-e3", "op-q", "op-wrk", "consume", SOLID + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"))
    c.append(edge("op-e4", "op-wrk", "op-sms", "send", ASYNC + "exitX=0.25;exitY=1;entryX=0.75;entryY=0;"))
    c.append(edge("op-e5", "op-wrk", "op-log", "record outcome", ASYNC))
    c.append(box("op-h2", "<b>Observability · Backup · Disaster Recovery</b>", 40, 475, 500, 26, style="fillColor=none;strokeColor=none;align=left;fontSize=13;"))
    c.append(box("op-zones", "<b>All zones</b><br>app · data · integration · edge", 60, 515, 190, 60, fill="#DAE8FC", stroke="#6C8EBF"))
    c.append(box("op-mon", "<b>Monitoring / SIEM</b><br>metrics · alerts · central logs", 340, 515, 190, 60, fill="#F5F5F5", stroke="#666666"))
    c.append(box("op-aud", "<b>Audit &amp; Config History</b>", 610, 515, 190, 60, fill="#D5E8D4", stroke="#82B366"))
    c.append(box("op-db", "Primary DB", 60, 640, 140, 60, fill="#D5E8D4", stroke="#82B366", style=DB))
    c.append(box("op-bak", "<b>Backup Storage</b><br>daily + PITR · restore testing", 340, 640, 200, 60, fill="#D5E8D4", stroke="#82B366"))
    c.append(box("op-dr", "<b>DR Site — failover</b><br>RPO / RTO pending NDC/BCC", 610, 640, 200, 60, style=PENDING))
    c.append(edge("op-e6", "op-zones", "op-mon", "ship logs / metrics", ASYNC + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"))
    c.append(edge("op-e7", "op-zones", "op-aud", "audit trail", ASYNC + "exitX=1;exitY=0.25;entryX=0;entryY=0.5;", points=[(300, 530), (300, 495), (570, 495), (570, 545)]))
    c.append(edge("op-e8", "op-db", "op-bak", "backups + WAL", SOLID + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"))
    c.append(edge("op-e9", "op-bak", "op-dr", "replicate (pending)", ASYNC + "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"))
    c.append(edge("op-e10", "op-mon", "op-dr", "failover trigger", ASYNC + "exitX=0.75;exitY=1;entryX=0.25;entryY=0;", points=[(482, 605), (660, 605)]))
    return c

# --- page 0: AWS cloud system design ----------------------------------------
def aws_icon(parent, id_, shape, label, x, y, w=70, h=60):
    st = (f"sketch=0;html=1;verticalLabelPosition=bottom;verticalAlign=top;outlineConnect=0;"
          f"shape=mxgraph.{shape};fillColor=#FFCC99;strokeColor=#000000;fontSize=9;whiteSpace=wrap;labelBackgroundColor=none;")
    return (f'<mxCell id="{id_}" value="{esc(label)}" style="{st}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

def page_aws():
    c = []
    # externals
    c.append(box("aws-users", "<b>Learners / Admins</b>", 40, 80, 120, 50, fill="#F5F5F5", stroke="#666666", style="ellipse;shape=cloud;"))
    c.append(box("aws-sso", "<b>BTP SSO / Identity</b><br><i>external IdP</i>", 210, 75, 160, 55, fill="#E1D5E7", stroke="#9673A6"))
    c.append(box("aws-pay", "<b>Payment</b><br><i>future</i>", 420, 75, 120, 50, style=PENDING))
    # aws cloud
    c.append(frame("aws-cloud", "AWS Cloud — Primary Region", 40, 155, 760, 620, fill="#FFFFFF", stroke="#999999"))
    c.append(aws_icon("aws-cloud", "aws-r53", "aws3.route_53", "Route 53", 20, 30, 70, 60))
    c.append(aws_icon("aws-cloud", "aws-cf", "aws3.cloudfront", "CloudFront CDN", 130, 30, 70, 60))
    c.append(svc("aws-cloud", "aws-waf", "AWS WAF + Shield", 245, 40, 120, 45, fill="#FFF2CC", stroke="#D6B656"))
    c.append(svc("aws-cloud", "aws-secret", "Secrets Manager · KMS · IAM", 420, 40, 150, 45, fill="#FFF2CC", stroke="#D6B656"))
    # vpc
    c.append(frame("aws-vpc", "VPC", 15, 110, 730, 400, fill="#F5F5F5", stroke="#666666", parent="aws-cloud"))
    c.append(frame("aws-pub", "Public Subnets", 10, 28, 710, 88, fill="#FFF2CC", stroke="#D6B656", parent="aws-vpc"))
    c.append(aws_icon("aws-pub", "aws-elb", "aws3.elastic_load_balancing", "Elastic Load Balancer", 290, 14, 110, 55))
    c.append(frame("aws-az1", "Private Subnet · AZ-1", 10, 126, 345, 142, fill="#DAE8FC", stroke="#6C8EBF", parent="aws-vpc"))
    c.append(aws_icon("aws-az1", "aws-ec2a", "aws3.ec2", "App Server 1 (EC2)", 30, 25, 70, 60))
    c.append(aws_icon("aws-az1", "aws-lam1", "aws4.lambda_function", "Workers 1 (Lambda)", 200, 25, 70, 60))
    c.append(svc("aws-az1", "aws-nat", "NAT Gateway — egress only", 120, 105, 190, 30, fill="#FFFFFF", stroke="#6C8EBF", style="fontSize=9;"))
    c.append(frame("aws-az2", "Private Subnet · AZ-2", 365, 126, 345, 142, fill="#DAE8FC", stroke="#6C8EBF", parent="aws-vpc"))
    c.append(aws_icon("aws-az2", "aws-ec2b", "aws3.ec2", "App Server 2 (EC2)", 40, 25, 70, 60))
    c.append(aws_icon("aws-az2", "aws-lam2", "aws4.lambda_function", "Workers 2 (Lambda)", 220, 25, 70, 60))
    c.append(frame("aws-data", "Data & Storage Subnets", 10, 278, 710, 110, fill="#D5E8D4", stroke="#82B366", parent="aws-vpc"))
    c.append(aws_icon("aws-data", "aws-rds", "aws3.rds", "RDS Primary · Multi-AZ", 15, 15, 70, 60))
    c.append(aws_icon("aws-data", "aws-rdsr", "aws3.rds", "RDS Read Replica", 105, 15, 70, 60))
    c.append(aws_icon("aws-data", "aws-cache", "aws3.elasticache", "ElastiCache Redis", 195, 15, 70, 60))
    c.append(aws_icon("aws-data", "aws-os", "aws3.cloudsearch", "Managed Search (OpenSearch)", 285, 15, 70, 60))
    c.append(aws_icon("aws-data", "aws-s3", "aws3.s3", "S3 — media · certificates", 375, 15, 70, 60))
    c.append(aws_icon("aws-data", "aws-sqs", "aws3.sqs", "SQS — job queue", 465, 15, 70, 60))
    # ops & security row
    c.append(frame("aws-ops", "Security & Operations", 15, 505, 730, 80, fill="#E1D5E7", stroke="#9673A6", parent="aws-cloud"))
    c.append(aws_icon("aws-ops", "aws-cw", "aws4.cloudwatch", "CloudWatch", 15, 8, 70, 60))
    c.append(aws_icon("aws-ops", "aws-backup", "aws3.s3", "AWS Backup · PITR", 190, 8, 70, 60))
    c.append(aws_icon("aws-ops", "aws-ses", "aws4.simple_email_service", "SES · email", 365, 8, 70, 60))
    c.append(aws_icon("aws-ops", "aws-sns", "aws4.sns", "SNS · SMS", 530, 8, 70, 60))
    c.append(aws_icon("aws-ops", "aws-sm", "aws4.secrets_manager", "Secrets Mgr", 655, 8, 70, 60))
    # DR row
    c.append(box("aws-dr", "<b>DR — Secondary AWS Region</b>: cross-region S3 replication · RDS read replica in DR · Route 53 failover — <i>RPO / RTO pending NDC/BCC</i>", 15, 592, 730, 24, style=PENDING))
    c[-1] = c[-1].replace('parent="1"', 'parent="aws-cloud"', 1)
    # edges
    c.append(edge("aws-e1", "aws-users", "aws-r53", "DNS"))
    c.append(edge("aws-e2", "aws-r53", "aws-cf", "HTTPS"))
    c.append(edge("aws-e3", "aws-cf", "aws-waf", "filtered"))
    c.append(edge("aws-e4", "aws-waf", "aws-elb", "443"))
    c.append(edge("aws-e5", "aws-elb", "aws-ec2a", ""))
    c.append(edge("aws-e6", "aws-elb", "aws-ec2b", ""))
    c.append(edge("aws-e7", "aws-ec2a", "aws-rds", "SQL"))
    c.append(edge("aws-e8", "aws-ec2b", "aws-rds", "SQL"))
    c.append(edge("aws-e9", "aws-rds", "aws-rdsr", "read replicas"))
    c.append(edge("aws-e10", "aws-ec2a", "aws-cache", "cache"))
    c.append(edge("aws-e11", "aws-ec2b", "aws-s3", "media · certificates"))
    c.append(edge("aws-e12", "aws-lam1", "aws-sqs", "consume", ASYNC))
    c.append(edge("aws-e13", "aws-lam2", "aws-ses", "email", ASYNC))
    c.append(edge("aws-e14", "aws-lam2", "aws-sns", "SMS", ASYNC))
    c.append(edge("aws-e15", "aws-az1", "aws-sso", "OIDC / SAML — SSO · profile sync (protocol pending ARCH)", SOLID + "exitX=0;exitY=0.25;entryX=0;entryY=0.5;", points=[(30, 420), (30, 102)]))
    c.append(edge("aws-e17", "aws-az2", "aws-cw", "logs / metrics / audit", ASYNC + "exitX=1;exitY=0.5;entryX=1;entryY=0.5;", points=[(845, 458), (845, 683)]))
    c.append(edge("aws-e18", "aws-rds", "aws-backup", "snapshots + WAL", ASYNC + "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"))
    return c

PAGES = [
    ("aws",   "0 · AWS Cloud System Design",                 "§13 · AWS deployment (stakeholder-approved)", page_aws),
    ("ctx",   "1 · System Context (C4 Level 1)",             "§4, §5.15",   page_ctx),
    ("comp",  "2 · Logical Component Architecture",          "§5, §7",      page_comp),
    ("net",   "3 · Network / Deployment Architecture",       "§13",         page_net),
    ("erd1",  "4 · Core Data Model — Learning Domain",       "§7",          page_erd1),
    ("erd2",  "5 · Core Data Model — Platform & Audit",      "§7",          page_erd2),
    ("state", "6 · State / Lifecycle Diagram",               "§5.3–5.6",    page_state),
    ("seq1",  "7 · Sequence — Auth & SSO",                   "§5.2",        page_seq1),
    ("seq2",  "8 · Sequence — Learning Lifecycle",           "§5.5–5.9",    page_seq2),
    ("seq3",  "9 · Sequence — Content Publishing",           "§5.3–5.4",    page_seq3),
    ("ops",   "10 · Integration, Observability, Backup & DR","§5.15–5.16, §13", page_ops),
]

def build():
    diagrams = []
    for i, (pid, title, srs, fn) in enumerate(PAGES, 1):
        cells = page_frame(pid, title, srs)
        cells += fn() if fn else placeholder(pid)
        body = "\n        ".join(cells)
        diagrams.append(f'''  <diagram id="btp-{i:02d}-{pid}" name="{esc(title)}">
    <mxGraphModel dx="1400" dy="850" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="826" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {body}
      </root>
    </mxGraphModel>
  </diagram>''')
    xml = ('<mxfile host="Electron" agent="claude-code" version="31.5.2" type="device" compressed="false">\n'
           + "\n".join(diagrams) + "\n</mxfile>\n")
    with open(OUT, "w") as f:
        f.write(xml)
    print(f"wrote {OUT} ({len(PAGES)} pages)")

if __name__ == "__main__":
    build()
