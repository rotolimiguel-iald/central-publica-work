"""Offline semantic narration revision; never synthesizes speech or changes scientific data."""
from pathlib import Path
import copy, json, os, re, sys, textwrap, time
import rebind_audio_v402 as c
import audio_v402_revision as revision

LANGS=('en','pt-BR','fr','zh-Hans')
EDITS=[]

def edit(films,key,index,texts,reason,anchors):
    assert len(texts)==4
    EDITS.append({'films':films,'segment':key,'cue_index':index,'text':dict(zip(LANGS,texts)),
                  'reason':reason,'anchors':anchors})

edit(('film1','film2'),'the_one',0,(
 'Teoria da Gravitação Luminodinâmica. The starting postulate assigns the identity operator value {omega_I} in the state. We follow that preserved identity.',
 'Teoria da Gravitação Luminodinâmica. O postulado inicial atribui valor {omega_I} ao operador identidade no estado. Seguimos essa identidade preservada.',
 'Teoria da Gravitação Luminodinâmica. Le postulat initial attribue la valeur {omega_I} à l’opérateur identité dans l’état. Nous suivons cette identité préservée.',
 '光动力学引力理论。起始公设规定：恒等算符在该状态中的值为 {omega_I}。接下来追踪这一保持不变的恒等性。'),
 'Explicar a normalização do estado e o papel do operador identidade, sem recitar ômega e I.',
 ['hud.items[omega_I]','cinema.formulas1[0]','Atlas.I.3'])
edit(('film1','film2'),'the_one',1,(
 'This geometry illustrates an ontological reading; the cosmic setting serves the presentation. Now the boundary takes shape.',
 'Esta geometria ilustra uma leitura ontológica; o cenário cósmico serve à apresentação. Agora a fronteira toma forma.',
 'Cette géométrie illustre une lecture ontologique ; le décor cosmique sert la présentation. La frontière prend maintenant forme.',
 '这里的几何呈现一种本体论解读；宇宙背景用于展示。现在，边界开始成形。'),
 'Preservar a declaração inicial ONTO/INPUT em prosa; não vocalizar siglas como fragmentos.',
 ['baseline.opening_scope','scene.alpha_source_note'])
edit(('film1','film2'),'boundary',1,(
 'Here, boundary entropy is {S_boundary} nat. Exponentiating it gives the minimum volume: the square root of Euler’s number.',
 'Aqui, a entropia da fronteira é {S_boundary} nat. A exponencial desse valor dá o volume mínimo: a raiz quadrada do número de Euler.',
 'Ici, l’entropie de frontière vaut {S_boundary} nat. Son exponentielle donne le volume minimal : la racine carrée du nombre d’Euler.',
 '这里，边界熵为 {S_boundary} 纳特。对它取指数，得到最小体积：欧拉数的平方根。'),
 'Distinguir entropia de número de Euler: o volume mínimo é a exponencial da entropia, que aqui resulta em √e.',
 ['Atlas.I.3','hud.items[S_boundary]','hud.items[sqrt_e]'])
edit(('film1','film2'),'mirror',0,(
 'The fine-structure constant, supplied externally, multiplies the square root of Euler’s number, giving the TGL coupling rate, beta TGL.',
 'A constante da estrutura fina, fornecida externamente, multiplica a raiz quadrada do número de Euler, dando a taxa de acoplamento beta TGL.',
 'La constante de structure fine, fournie extérieurement, multiplie la racine carrée du nombre d’Euler et donne le taux de couplage TGL, bêta TGL.',
 '精细结构常数作为外部输入，乘以欧拉数的平方根，给出 TGL 耦合率，即 beta TGL。'),
 'Nomear a constante e a taxa pelo papel; α continua entrada externa e β derivado. O valor numérico de β permanece no HUD com sua precisão original.',
 ['Atlas.I.3','scene.alpha_source_note','hud.items[beta]'])
edit(('film1','film2'),'mirror',1,(
 'It sets the reflected share; transmission carries the rest. The projection angle is {theta_M} degrees.',
 'Ela fixa a parcela refletida; a transmissão leva o restante. O ângulo de projeção é {theta_M} graus.',
 'Il fixe la part réfléchie ; la transmission porte le reste. L’angle de projection vaut {theta_M} degrés.',
 '它确定反射份额，其余部分透射。投影角为 {theta_M} 度。'),
 'Explicar a repartição de pesos e o ângulo como leitura; a fórmula matricial continua visível, sem leitura de letras.',
 ['Atlas.I.3','cinema.formulas2[2]','hud.items[tau_trans]'])
edit(('film1',),'face',1,(
 'Powers links the scales. The density distributes the zero mode’s weight, separated from the other modes by Breuer’s local gap.',
 'Powers liga as escalas. A densidade distribui o peso do modo zero, separado dos demais pelo gap local de Breuer.',
 'Powers relie les échelles. La densité répartit le poids du mode zéro, séparé des autres modes par le gap local de Breuer.',
 'Powers 阶梯连接不同尺度。密度分布描述零模的权重；Breuer 局部能隙将它与其他模分开。'),
 'Explicar a densidade mostrada como peso do modo zero na coordenada modular, sem identificá-la com densidade material ou energia.',
 ['frames.breuer.density','frames.breuer.k','core.local_breuer_gap.statuses.zero_mode_weight','core.local_breuer_gap.checks'])
edit(('film1','film2'),'light',0,(
 'Applying the reflection operation twice restores identity. Conjugation reverses the generator, so the displayed gradient reverses direction.',
 'Aplicar a operação de reflexão duas vezes restaura a identidade. A conjugação inverte o gerador; assim, o gradiente exibido muda de sentido.',
 'Appliquer deux fois l’opération de réflexion rétablit l’identité. La conjugaison inverse le générateur : le gradient affiché change donc de sens.',
 '连续施加两次反射操作会恢复恒等作用。共轭使生成元反号，因此画面中的梯度方向反转。'),
 'Explicar J²=I e JKJ=−K como operações. A leitura de Luz é ontológica; não identificar J com um novo campo físico nem K com portador de luz.',
 ['Atlas.I.5','core.light_is_J.checks','cinema.formulas1[4]'])
edit(('film1',),'gravity',0,(
 'Soldering connects the local frame to transport. Changing the order leaves a rotation; a small loop reveals curvature.',
 'A solda liga o referencial local ao transporte. Mudar a ordem deixa uma rotação; um pequeno circuito revela a curvatura.',
 'La soudure relie le repère local au transport. Changer l’ordre laisse une rotation ; un petit circuit révèle la courbure.',
 '焊接把局部标架与输运连接起来。交换顺序会留下旋转；沿小回路输运则显出曲率。'),
 'Descrever o efeito do comutador e do circuito em lugar de ler índices; os geradores de Lorentz não são confundidos com a conjugação modular.',
 ['cinema.formulas1[5]','core.solder_4d','core.minimal_solder'])
edit(('film2',),'sheet',0,(
 'The density curve shows how the zero mode’s weight is distributed along the modular coordinate. Breuer’s local gap separates it from the other modes.',
 'A curva de densidade mostra como o peso do modo zero se distribui na coordenada modular. O gap local de Breuer o separa dos demais modos.',
 'La courbe de densité montre la répartition du poids du mode zéro selon la coordonnée modulaire. Le gap local de Breuer le sépare des autres modes.',
 '密度曲线展示零模权重沿模坐标的分布。Breuer 局部能隙把它与其他模分开。'),
 'Precisar a grandeza da curva e o caráter local do gap; não criar identificação com densidade material.',
 ['frames.breuer.density','core.local_breuer_gap.statuses.zero_mode_weight','core.local_breuer_gap.statuses.wall_corrected'])
edit(('film2',),'sheet',1,(
 'The Powers ladder links scales; the coframe supplies local directions. Changes of frame in different directions depend on their order, leaving the rotation shown in the Lorentz relation.',
 'A cadeia de Powers liga escalas; o coframe fornece direções locais. Mudanças de referencial em direções diferentes dependem da ordem, deixando a rotação mostrada na relação de Lorentz.',
 'L’échelle de Powers relie les échelles ; le corepère fournit les directions locales. Les changements de repère selon différentes directions dépendent de leur ordre, laissant la rotation de la relation de Lorentz.',
 'Powers 阶梯连接尺度；余标架提供局部方向。沿不同方向改变标架，结果依赖操作顺序，从而留下洛伦兹关系中显示的旋转。'),
 'Explicar coframe e não comutatividade que a cena mostra, preservando o encadeamento sem ler K e J como se fossem o mesmo objeto de outras cenas.',
 ['cinema.formulas2[4]','core.solder_4d'])
edit(('film2',),'transport',0,(
 'Soldering links the frame to geometry. The generators describe infinitesimal changes of frame; their order leaves the rotation measured by the commutator.',
 'A solda liga o referencial à geometria. Os geradores descrevem mudanças infinitesimais de referencial; a ordem dessas operações deixa a rotação medida pelo comutador.',
 'La soudure relie le repère à la géométrie. Les générateurs décrivent des changements infinitésimaux de repère ; leur ordre laisse la rotation mesurée par le commutateur.',
 '焊接把标架与几何连接起来。生成元描述标架的无穷小变化；操作顺序留下的旋转由对易子刻画。'),
 'Dar sentido aos operadores e ao comutador pela diferença entre ordens de operação.',
 ['core.solder_4d','cinema.formulas2[4]'])
edit(('film2',),'transport',1,(
 'The loop’s mismatch measures holonomy. The curvature formula relates it to the product of the generator coefficients.',
 'O desajuste ao fechar o circuito mede a holonomia. A fórmula da curvatura o relaciona ao produto dos coeficientes dos geradores.',
 'L’écart à la fermeture du circuit mesure l’holonomie. La formule de courbure le relie au produit des coefficients des générateurs.',
 '回路闭合时的偏差刻画整体输运效应，即 holonomy。曲率公式把它与生成元系数的乘积联系起来。'),
 'Explicar a operação e o significado de R=2c₁c₂; o fator e a expressão permanecem visíveis, sem novo valor falado.',
 ['cinema.formulas2[5]','core.minimal_solder'])
edit(('film2',),'spin',0,(
 'Spin describes how the tensor responds when the frame rotates. Opposite helicities give {pol} transverse polarizations.',
 'O spin descreve como o tensor responde à rotação do referencial. Helicidades opostas dão {pol} polarizações transversais.',
 'Le spin décrit la réponse du tenseur à la rotation du repère. Des hélicités opposées donnent {pol} polarisations transverses.',
 '自旋描述张量对标架旋转的响应。相反的螺旋度给出 {pol} 个横向偏振。'),
 'Explicar spin pela lei de transformação, sem recitar índices ou acrescentar observação física.',
 ['cinema.formulas2[7]','core.graviton_polarization'])
edit(('film2',),'einstein',0,(
 'H₁ supplies a finite trace and a local gap; H₂, coframe and Lorentz; H₃, horizon and Clausius. These assemble the Pentad.',
 'H₁ fornece traço finito e gap local; H₂, coframe e Lorentz; H₃, horizonte e Clausius. Assim se compõe a Pêntada.',
 'H₁ fournit une trace finie et un gap local ; H₂, corepère et Lorentz ; H₃, horizon et Clausius. Ainsi s’assemble la Pentade.',
 'H₁ 提供有限迹和局部能隙；H₂ 提供余标架与洛伦兹结构；H₃ 提供视界与克劳修斯关系。它们组合成五元组。'),
 'Preservar os três contratos e nomes, apenas explicitar finitude do traço e alcance local do gap.',
 ['baseline.hypothesis_contract','core.local_breuer_gap','core.triad_master'])

# Keep the complete Adendo D opening in all four languages while explaining the test quantities.
for film,key,prefix in [('film1','nature',False),('film2','identity',True)]:
    beginnings=(
      'Identity returns with residual {id_true}. ' if prefix else '',
      'A identidade retorna com resíduo {id_true}. ' if prefix else '',
      'L’identité revient avec un résidu de {id_true}. ' if prefix else '',
      '恒等返回的残差为 {id_true}。' if prefix else '')
    edit((film,),key,0,tuple(a+b for a,b in zip(beginnings,(
      'The three supports count together, each with its own status: calibrated separation {z_disc}, one-sided probability {p_disc}, threshold {threshold_sigma} sigma. The result remains below it.',
      'Os três apoios contam juntos, cada um com o seu estatuto: separação calibrada {z_disc}, probabilidade unilateral {p_disc}, limiar {threshold_sigma} sigma. O resultado permanece abaixo dele.',
      'Les trois appuis comptent ensemble, chacun avec son propre statut : séparation calibrée {z_disc}, probabilité unilatérale {p_disc}, seuil {threshold_sigma} sigma. Le résultat reste en dessous.',
      '三个支撑共同发挥作用，各自保有其地位：校准后的区分度为 {z_disc}，单侧概率为 {p_disc}，阈值为 {threshold_sigma} sigma。结果仍低于阈值。'))),
      'Preservar D e os valores/limiar no mesmo trecho, substituindo letras isoladas pelo papel das grandezas; nenhum apoio é somado ou multiplicado.',
      ['core.teste_de_veracidade_fase9_v397.lido','core.teste_de_veracidade_fase9_v397.nao_diz','AdendoD'])
    edit((film,),key,1,(
      'The model’s offset is {z_delta}: not falsified with power. Bayesian evidence uses another scale. Kernel validity holds under hypotheses; nature decides.',
      'O desvio do modelo é {z_delta}: não falsificada com poder. Evidência bayesiana usa outra escala. Validade no kernel sob hipóteses; a natureza decide.',
      'L’écart du modèle vaut {z_delta} : non falsifiée avec puissance. L’évidence bayésienne utilise une autre échelle. Validité dans le noyau sous hypothèses ; la nature tranche.',
      '模型偏差为 {z_delta}：在有检验功效的条件下未被证伪。贝叶斯证据采用另一种尺度。内核有效性成立于假设之下；自然裁决。'),
      'Explicar o desvio e separar a escala bayesiana; preservar a conclusão delimitada ao kernel sob hipóteses.',
      ['core.teste_de_veracidade_fase9_v397.lido','core.teste_de_veracidade_fase9_v397.nao_diz','baseline.closing_scope'])


def write_versioned(path,body):
    revision.stable_new(c,path,body)


def caption_chunks(text, language):
    # Reading preview only: no fabricated speech alignment or playback timestamps.
    limit=32 if language=='zh-Hans' else 84
    if language=='zh-Hans':
        phrases=re.findall(r'.*?[，。；：！？]|.+$',text)
        chunks=[];buf=''
        for phrase in phrases:
            if buf and len(buf+phrase)>limit:chunks.append(buf);buf=''
            buf+=phrase
        if buf:chunks.append(buf)
        return chunks
    return textwrap.wrap(text,width=limit,break_long_words=False,break_on_hyphens=False)


def main():
    preflight=c.check();data=revision.data_gate(c);guard=revision.seal_guard(c);builder=c.builder_module()
    prior_template=c.C/'AUDIO_SCRIPT_TEMPLATES_V402.json';previous=c.old.read(prior_template)
    revised=copy.deepcopy(previous);changes=[];lookup={}
    for item in EDITS:
        for film in item['films']:
            seg=next(s for s in revised['films'][film]['segments'] if s['key']==item['segment'])
            i=item['cue_index'];lookup[(film,item['segment'],i)]=item
            for lang in LANGS:
                before=seg['text'][lang][i];after=item['text'][lang]
                assert before!=after,(film,item['segment'],i,lang)
                seg['text'][lang][i]=after
                changes.append({'film':film,'segment':item['segment'],'cue_index':i,'language':lang,
                    'old_template':before,'new_template':after,'reason':item['reason'],'anchors':item['anchors']})
    revised['revision']='V402_FORMULA_R1_SEMANTIC_NARRATION_ADENDO_D_PRESERVED'
    revised['hud_only_fields']=sorted(set(revised['hud_only_fields']+['beta']))
    builder.validate_templates(revised)
    template=c.C/'AUDIO_SCRIPT_TEMPLATES_V402_FORMULA_R1.json';write_versioned(template,revised)
    with c.old.local_only():
        plan=builder.make_plan(c.V,template)
        mechanics=builder.self_test(revised)
    previous_plan=c.old.read(c.C/'AUDIO_PLAN_V402_CANDIDATE.json')
    baseline=c.old.read(c.C/'baseline_audio_v401/audio/NARRATION_PLAN_v401_final.json')
    old_units=revision.units(builder,baseline);current=revision.units(builder,plan)
    for key,unit in current.items():
        hit=builder.completed_cached_audio(builder.io_path(c.V/'audio/cache'),key)
        unit['unchanged_from_v401']=key in old_units
        unit['completed_cache']=None if hit is None else {'audio':c.old.pin(hit),'receipt':c.old.pin(hit.with_suffix('.json'))}
        if key in old_units:assert hit is not None
    all_cues=[];affected=[];captions=[];budgets=[]
    for film,content in plan['films'].items():
        assert content['total_seconds']==previous_plan['films'][film]['total_seconds']
        for segment,old_segment in zip(content['segments'],previous_plan['films'][film]['segments']):
            for field in ('start','end','duration','key','source_key','index'):assert segment[field]==old_segment[field]
            budgets.append({'film':film,'segment':segment['key'],'start':segment['start'],'end':segment['end'],
                            'budget':segment['speech_budget']})
            for index,(new,old) in enumerate(zip(segment['cues'],old_segment['cues'])):
                item=lookup.get((film,segment['key'],index))
                row={'film':film,'segment':segment['key'],'cue_index':index,'changed_by_formula_revision':item is not None,
                     'old':{k:old[k] for k in ('pt-BR','en')},'new':{k:new[k] for k in ('pt-BR','en')},
                     'translations':new,'reason':item['reason'] if item else 'Mantida: já descreve significado/efeito, preserva contrato H₁/H₂/H₃ ou correção D.',
                     'anchors':item['anchors'] if item else ['baseline_same_cue','current_hud','AdendoD'],
                     'segment_budget':segment['speech_budget']}
                all_cues.append(row)
                if item:affected.append(row)
                captions.append({'film':film,'segment':segment['key'],'cue_index':index,
                                 'reading_chunks':{lang:caption_chunks(text,lang) for lang,text in new.items()}})
    # D wording/counts survive; numerical speech remains a selected HUD substitution.
    for film,key,index in [('film1','return',0),('film2','einstein',1)]:
        seg=next(s for s in revised['films'][film]['segments'] if s['key']==key)
        assert seg['text']==next(s for s in previous['films'][film]['segments'] if s['key']==key)['text'] if key=='return' else all(seg['text'][lang][index]==next(s for s in previous['films'][film]['segments'] if s['key']==key)['text'][lang][index] for lang in LANGS)
    for film,key in [('film1','nature'),('film2','identity')]:
        seg=next(s for s in revised['films'][film]['segments'] if s['key']==key)
        for lang,pairs in revision.REPLACEMENTS.items():assert pairs[1][1] in seg['text'][lang][0]
    for film in plan['films']:
        for seg in plan['films'][film]['segments']:
            assert not any(re.search(r'\b(?:alpha|alfa|omega|ômega)\b|square root of e\b|raiz quadrada de e\b|\bJ composed|\bJ composto',cue[lang],re.I) for cue in seg['cues'] for lang in ('en','pt-BR'))
    planned=c.C/'AUDIO_PLAN_V402_FORMULA_R1.json';write_versioned(planned,plan)
    public_template=c.V/'audio/script_templates.json';raw=template.read_bytes()
    if public_template.read_bytes()!=raw:
        assert c.old.digest(public_template) in {c.old.digest(c.C/'baseline_audio_v401/audio/script_templates.json'),c.old.digest(prior_template)}
        backup=public_template.with_name(public_template.name+'.bak_before_formula_'+str(time.time_ns()))
        backup.write_bytes(public_template.read_bytes());tmp=public_template.with_suffix('.tmp_formula');tmp.write_bytes(raw)
        assert tmp.read_bytes()==raw;os.replace(tmp,public_template)
    final_plan=c.V/'audio/NARRATION_PLAN_v402_formula_final.json';write_versioned(final_plan,plan)
    assert builder.make_plan(c.V,public_template)==plan
    counts={'unique_units':len(current),'cue_occurrences':sum(len(u['occurrences']) for u in current.values()),
            'new_v402_units':sum(not u['unchanged_from_v401'] for u in current.values()),
            'reused_v401_units':sum(u['unchanged_from_v401'] for u in current.values()),
            'new_units_missing_audio':sum(u['completed_cache'] is None for u in current.values()),
            'reviewed_cue_pairs':len(all_cues),'affected_cue_pairs':len(affected),'changed_strings_four_languages':len(changes)}
    source_paths=[c.V/'data/hud.json',c.V/'data/frames.json',c.V/'source/um_absoluto.json',c.V/'cinema/timeline.mjs',
                  Path('C:/IALD/Central de Patentes/memory/TGL_ATLAS.md')]
    operator=c.C/'OPERATOR_FORMULA_NARRATION.txt';assert operator.exists(),'PARENT_OPERATOR_SOURCE_MISSING'
    report={'schema':'iald.formula-narration-review.v402/v1','status':'CANDIDATE_AWAITING_PARENT_TEXT_REVIEW_NO_TTS',
        'actor':c.ACTOR,**guard,'preflight':preflight,'operator_order':c.old.pin(operator),
        'corrections_order':c.old.read(c.C/'SOURCE_INTAKE.json')['corrections'],
        'plan_sha256':plan['plan_sha256'],'plan':c.old.pin(final_plan),'candidate_plan':c.old.pin(planned),
        'templates':c.old.pin(public_template),'versioned_templates':c.old.pin(template),
        'previous_plan_preserved':c.old.pin(c.C/'AUDIO_PLAN_V402_CANDIDATE.json'),'previous_templates_preserved':c.old.pin(prior_template),
        'data_ready':c.old.pin(c.C/'DATA_READY.json'),'parent_numeric_review':c.old.pin(c.C/'PARENT_NUMERIC_REVIEW.json'),
        'counts':counts,'all_cues_reviewed':all_cues,'affected_cues':affected,'template_changes':changes,
        'units':list(current.values()),'timing_budget':budgets,
        'timing_warnings':[{'film':b['film'],'segment':b['segment'],'language':lang,**value} for b in budgets for lang,value in b['budget'].items() if value['may_need_extension']],
        'durations_unchanged':{f:d['total_seconds'] for f,d in plan['films'].items()},
        'spoken_number_policy':{'numeric_values_modified':False,'beta_numeric_value_moved_to_hud_only':True,
            'reason':'Voice explains the coupling construction; original 12-digit HUD beta remains unchanged. Projection angle and other spoken values still come from HUD.',
            'p_format':revised['formats']['p_disc']},
        'adendo_d_checked_by_builder':True,'hypothesis_contracts_preserved':True,
        'translation_alignment_checked_by_builder':True,'independent_translation_review_pending':True,
        'source_pins':[c.old.pin(p) for p in source_paths],
        'source_sections':['Atlas I.3 and I.5; current lines 678–727','core.light_is_J','core.local_breuer_gap','core.solder_4d','core.minimal_solder','core.graviton_polarization','core.teste_de_veracidade_fase9_v397.lido'],
        'semantic_separations':['Euler’s number is not entropy; exp(boundary entropy)=sqrt(e) in this construction.',
           'Fine-structure constant is INPUT/KNOWN; coupling beta is DERIVED.',
           'Modular density means the zero-mode weight profile, not material/energy density.',
           'Modular conjugation J and Lorentz rotation generator J3 are distinct objects.',
           'The compact angle reads the hyperbolic face; it is not the face.',
           'The three supports retain distinct status and are not added or multiplied.'],
        'subtitle_policy':{'four_languages_follow_exact_speech':True,'formula_recitation_removed':True,
            'reading_chunks_preview':str(c.C/'FORMULA_SUBTITLE_READING_PREVIEW.json'),
            'timings':'No invented alignment; final subtitle timing requires measured speech after authorization.',
            'display':'Short reading blocks proposed; no formula duplicated in captions when voice explains its meaning.'},
        'offline_checks':mechanics,'network_calls':0,'tts_calls':0,'audio_inflight':False,
        'audio_mixes_subtitles_timelines_untouched':True,'perceptual_audition':False,
        'limitations':['Timing is a conservative text estimate, not measured voice.','Parent review and separate human authorization gate synthesis.','No new physics or scientific proof is asserted.']}
    revision.seal_guard(c)
    c.old.write_new(c.C/'FORMULA_SUBTITLE_READING_PREVIEW.json',{'status':'UNTIMED_READING_PREVIEW','plan_sha256':plan['plan_sha256'],'items':captions})
    c.old.write_new(c.C/'FORMULA_NARRATION_REVIEW.json',report)
    print(json.dumps({'status':report['status'],'plan_sha256':plan['plan_sha256'],'counts':counts,'warnings':report['timing_warnings'],
                      'review':c.old.pin(c.C/'FORMULA_NARRATION_REVIEW.json'),'plan':c.old.pin(final_plan),'templates':c.old.pin(public_template)},ensure_ascii=False))

if __name__=='__main__':main()
