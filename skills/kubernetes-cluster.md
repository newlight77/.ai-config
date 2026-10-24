# Kubernetes Cluster Skills (k3s, GitOps)

**When to use:** Any SSH, `kubectl`, secret sealing, Helm, Argo CD sync, Ansible node setup or rollout against a k3s / Kubernetes cluster. Read this skill **before** running cluster commands. The concrete cluster (provider, nodes, namespaces, repositories) is described by the project or platform skill, for Shipdeck `shipdeck-infra-skills.md`.

## Principle: rebuildable from the repositories

The infrastructure and the cluster must be recreatable from the repositories alone, so the whole stack can be redeployed quickly (for example when changing provider).

- Every change to a node or to the cluster is made **in code first** and committed:
  - node setup, k3s and kubelet arguments: Ansible (playbooks and `group_vars`; the real `hosts.yaml` is derived from `hosts.yaml.example` and stays gitignored);
  - everything that runs in the cluster: the config repository (Argo CD Applications, chart values, resources, sealed secrets) and the Helm charts.
- Argo CD runs with `selfHeal`: a live `kubectl edit` is reverted. **Change git, not the cluster.**
- A manual change on a node or in the cluster is allowed only as an emergency or a one-off (for example deleting a stuck pod). Reproduce it in code **in the same session**, and make the playbook idempotent so re-running it is a no-op.
- Never leave a setting that exists only on a machine. If a value, flag or secret cannot be reproduced from the repositories, record it (README or runbook) and, for secrets, in a sealed-secret inventory.
- Prefer provider-agnostic code: no provider-specific addresses or names outside the inventory. Keep the cluster rebuild runbook current when a step changes.

## Hard requirements (agent)

1. **Access is SSH by key only** (password authentication is deactivated). Read the control-node address from the gitignored Ansible inventory (`inventories/<env>/hosts.yaml`); never hardcode an address in prose, scripts or skills.
2. **Cluster access must run outside the sandbox.** In the Shell tool set `required_permissions: ["all"]` for `ssh`, `scp`, `docker`, `gpg`, `kubeseal` or anything that talks to the nodes. Do not retry sandboxed SSH hoping it works.
3. Use non-interactive SSH: `-o BatchMode=yes` (agent terminals cannot answer prompts; a missing key then fails fast). Nodes may be dual-stack; `-4` / `-6` both work.
4. On the control node use `sudo k3s kubectl …` unless a local kubeconfig is explicitly configured.
5. Stay **read-only** (`get`, `describe`, `logs`) until the change and the rollback path are clear.
6. Never commit or paste plaintext secrets. Git holds SealedSecret ciphertext only.

## Connect and inspect

```bash
ssh -o BatchMode=yes <operator>@<control-node> 'hostname; uptime'
ssh -o BatchMode=yes <operator>@<control-node> '
  sudo k3s kubectl get nodes -o wide
  sudo k3s kubectl -n <namespace> get deploy,po,svc
  sudo k3s kubectl -n <namespace> logs deploy/<app> --tail=80
'
```

Probe public health endpoints from the laptop (`curl -4sfS` / `curl -6sfS https://<host>/health`) before and after a change.

## How to apply changes (GitOps)

| Change type | Where | How it reaches the cluster |
|-------------|-------|----------------------------|
| Non-secret ConfigMap / Helm values | config repository, `environments/<ns>/` | commit, push, Argo CD sync |
| Secrets | config repository, `environments/<ns>/secrets/*.sealed.yaml` | seal locally, commit ciphertext, Argo CD |
| Image / app code | app repository CI | build, push, then a pin commit in the config repository (never `kubectl set image`) |
| Node setup | Ansible | run the playbook; keep it idempotent |
| Emergency one-off | control node | apply, then reconcile git in the same session |

Restart consumers after a Secret or ConfigMap env change so pods reload `envFrom`: `sudo k3s kubectl -n <ns> rollout restart deploy/<app>` then `rollout status … --timeout=180s`.

## Helm and Argo CD

- Charts live with the application code; the config repository holds per-environment values and the Argo CD Applications (app-of-apps root plus an AppProject).
- Check charts before they reach an environment: `helm lint`, `helm template` (same Helm version as Argo CD) and `kubeconform -strict` for every Application.
- Argo CD itself has no GitOps path: it must exist before anything can bootstrap. Public exposure of Argo CD, Prometheus and Loki is avoided; use SSH, `kubectl` or a local `port-forward`.

## Sealed Secrets (vault)

The private key stays **only on the cluster**. Fetch the sealing certificate over SSH (the API may be closed publicly):

```bash
ssh -o BatchMode=yes <operator>@<control-node> \
  'sudo k3s kubectl get secret -n kube-system \
    -l sealedsecrets.bitnami.com/sealed-secrets-key=active \
    -o jsonpath="{.items[0].data.tls\.crt}"' | base64 -d > sealed-secrets.pem
```

Seal a local `KEY=VALUE` file with the config repository's seal script. Merge incomplete seals carefully, never wipe live `DATABASE_URL` or signing keys. Keep plaintext `*.env` and the `.pem` gitignored, and keep a key-name inventory (`*.example.env`) beside the ciphertext so the whole vault can be resealed after a rebuild.

## Images / Docker

- Build on the laptop (`linux/amd64`) or on a self-hosted runner, not under load on the control node.
- Docker, SCP and SSH for any such path also require `required_permissions: ["all"]`.
- Where Argo CD manages a namespace, images reach it through a pin commit; direct `ctr import` / `set image` is refused.

## Safety do-nots

- No password SSH; no sandboxed Shell for cluster access.
- No `kubectl delete` / `drain` / blanket `edit` without a plan, preferably backed by a git change.
- No second ingress controller: k3s already ships Traefik in `kube-system`.
- No plaintext `.env` in the config repository.
- No lasting drift that only exists as a live edit.
