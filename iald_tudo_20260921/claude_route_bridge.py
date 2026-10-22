"""Prepared route boundary: select/inspect authenticated accounts without writes.

This uses the existing IALD account/consent/config API through an injected module.
No web server import, file reads, environment access or credential handling.
"""
from copy import copy, deepcopy
import math
from claude_profiles import HAIKU,SONNET
from claude_server_selection import select_fields,selected_model,option_rows,config_for_model

# Official Anthropic pricing checked 2026-09-22:
# https://platform.claude.com/docs/en/about-claude/pricing
# Ordering matches IALD: input, cache read, output, cache write (USD / 1M).
HAIKU_PRICES_5M=(1.0,0.10,5.0,1.25)
HAIKU_WRITE_1H=2.0

class RouteBridge:
    def __init__(self,*,motors,base_config,package_loader,enabled=False,
                 public_daily_usd=None,public_group_daily_usd=None):
        self.motors=motors;self.base=base_config;self.package_loader=package_loader
        if type(enabled)is not bool:raise ValueError('Explicit feature switch required')
        self.enabled=enabled
        self.public_daily_usd=public_daily_usd
        self.public_group_daily_usd=public_group_daily_usd

    def haiku_rates(self):
        rates=self.base.precos(HAIKU.model)
        if rates is None:
            rates=list(HAIKU_PRICES_5M)
            if self.base.cache_ttl=='1h':rates[3]=HAIKU_WRITE_1H
        if len(rates)!=4 or any(isinstance(p,bool) or not isinstance(p,(int,float))
                or not math.isfinite(p) or p<0 for p in rates):
            raise ValueError('Invalid Haiku prices')
        return tuple(rates)

    def public_budget(self):
        """No public spend until operator-configured amounts are usable.

        The existing global provider cap is never increased by this feature.
        Require room for one cold request; a zero/legacy two-cent quota must
        not masquerade as an available 180k-memory model.
        """
        amounts=(self.public_daily_usd,self.public_group_daily_usd,self.base.cota_global_usd)
        try:
            if any(isinstance(v,bool) for v in amounts):raise ValueError()
            daily,group,total=map(float,amounts)
            if any(not math.isfinite(v) for v in (daily,group,total)):raise ValueError()
            rates=self.haiku_rates()
            minimum=(200000*1.15*max(rates[0],rates[1],rates[3])+4096*rates[2])/1e6
            if not minimum<=daily<=group<=total:raise ValueError()
        except (ValueError,TypeError,IndexError):
            raise ValueError('Public Haiku budget not configured for this memory') from None
        return daily,group

    def package(self):
        if not self.enabled:raise ValueError('Haiku not activated')
        return self.package_loader()

    def flags(self):
        configured=self.motors.claude_configurado(self.base)
        ready=False
        if configured and self.enabled:
            try:self.package();ready=True
            except (ValueError,OSError,KeyError,UnicodeError):pass
        return dict(haiku_ready=ready,sonnet_ready=configured)

    def policy_flags(self,username):
        flags=self.flags()
        flags['sonnet_ready']=flags['sonnet_ready'] and str(username).strip().lower() in self.base.contas
        if str(username).strip().lower()!='luiz':
            try:self.public_budget()
            except ValueError:flags['haiku_ready']=False
        return flags

    def options(self,record,username):
        return option_rows(record,username,**self.policy_flags(username))

    def select(self,option_id,record,username):
        fields=select_fields(option_id,record,username,**self.policy_flags(username))
        # Caller persists only this result, after normal CSRF/session checks.
        return fields

    def model(self,record,username):
        return selected_model(record,username,**self.policy_flags(username))

    def selection_id(self,record,username):
        return 'claude-haiku' if self.model(record,username)==HAIKU.model else 'claude-sonnet'

    def configuration(self,record,username):
        model=self.model(record,username)
        cfg=self.motors.config_da_conta(self.base,record)
        if model==HAIKU.model:
            cfg.precos_tabela=dict(cfg.precos_tabela)
            # Preserve an explicitly configured server price; otherwise install
            # the verified defaults, matching the provider cache TTL.
            cfg.precos_tabela[model]=self.haiku_rates()
            if str(username).strip().lower()!='luiz':
                daily,group=self.public_budget()
                cfg.planos=deepcopy(cfg.planos)
                for limits in cfg.planos.values():limits['usd_dia']=daily
                cfg.cota_usuario_usd=cfg.cota_operador_usd=daily
                cfg.cota_global_gratuito_usd=group
                cfg.haiku_public_group_limit=group
                cfg.somente_limite_global=False
        return config_for_model(cfg,model)

    def consent(self,record):
        m=self.motors
        return {'necessario':True,'dado':m.consentiu(record,m.CLAUDE),
                'versao':m.versao_do_consentimento(m.CLAUDE),
                'texto':m.texto_do_consentimento(m.CLAUDE),
                'provedor':m.PROVEDORES[m.CLAUDE]}
