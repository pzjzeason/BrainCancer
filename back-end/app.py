from flask import Flask, request, jsonify
from flask_cors import CORS
from owlready2 import *
import copy
import json
import hashlib
import random
import requests
#

def yd(query):
    md5 = hashlib.md5()
    appKey = '2c19f05b741aab90'
    secretKey = 'CDiwoG6ZQoaGYuCXzjnNJqtpvVnn1Tg5'
    myurl = 'http://openapi.youdao.com/api'
    q = query
    fromLang = 'EN'
    toLang = 'zh-CHS'
    salt = random.randint(1, 65536)
    sign = appKey + q + str(salt) + secretKey
    md5.update(sign.encode('utf-8'))
    sign = md5.hexdigest()
    payload = {'appKey': appKey, 'q': q, 'from': fromLang, 'to': toLang, 'salt': str(salt), 'sign': sign}
    try:
        res = requests.get(myurl, params=payload)
        translation = res.json()['translation'][0]
        return translation
    except:
        print(query)
        print('state:' + str(res.status_code))
        return '暂缺'


def get_all_tumors():
    onto = get_ontology("file://./braincancer.owl").load()
    individuals_by_class = {}
    tumors = {}
    name_with_id = {}
    classes = {}
    tumor_id = 0
    class_id = 0
    tumor_classes = onto.search(subclass_of=onto.CentralNervousSystemTumours)
    for each in tumor_classes:
        individuals_by_class[each.nameInCn[0]] = [a for a in onto.search(type=each)]
    for e in individuals_by_class:
        classes['tumor_parent_' + str(class_id)] = {'name': e, 'children': []}
        for tumor in individuals_by_class[e]:
            name_with_id[tumor.name] = 'tumor_child_' + str(tumor_id)
            classes['tumor_parent_' + str(class_id)]['children'].append('tumor_child_' + str(tumor_id))
            tumor_content = {'tumorNameEn': tumor.name}
            for each in tumor.get_properties():
                if each == onto.nameAlso:
                    tumor_content['nameAlsoCn'] = [str(a) for a in each[tumor] if a.lang == 'cn']
                    tumor_content['nameAlsoEn'] = [str(a) for a in each[tumor] if a.lang == 'en']
                elif each == onto.definition:
                    tumor_content['definitionCn'] = [str(a) for a in each[tumor] if a.lang == 'cn']
                    tumor_content['definitionEn'] = [str(a) for a in each[tumor] if a.lang == 'en']
                else:
                    if each.name in ['hasHighOccurrenceRateIn', 'hasFindingSite', 'hasSymptoms', 'isDiagnosedBy',
                                     'associatedTumours']:
                        tumor_content[each.name] = [[a.name, onto.NameInCN[a][0]] for a in each[tumor]]
                    else:
                        tumor_content[each.name] = each[tumor]
            tumors['tumor_child_' + str(tumor_id)] = tumor_content
            tumor_id += 1
        class_id += 1
    with open('/Users/zeason/Documents/课程/大三下/KnowledgeBase/data/picture_describe.json', 'r') as f:
        pd = json.load(f)
    final_tumors_info = {}
    keys = dict.fromkeys(
        ['tumorNameEn', 'NameInCN', 'nameAlsoEn', 'nameAlsoCn', 'MeshCode', 'ICD_10Code', 'ICD_OCode',
         'MeshThematicWord', 'ICDThematicWord', 'definitionCn', 'definitionEn', 'isDefinedBy', 'OccurrenceRate',
         'hasHighOccurrenceRateIn', 'hasFindingSite', 'hasSymptoms',
         'Pathogeny', 'isDiagnosedBy', 'DifferentialDiagnosis', 'associatedTumours', 'OtherAssociatedIllness',
         'CTImageDescription', 'MRIImageDescription', 'CTImageDescriptionInCN', 'DifferentialDiagnosisInCN',
         'MRIImageDescriptionInCN', 'PathogenyInCN'], ['暂缺'])

    def ty(each,a):
        type_comment = comment[ onto.search(iri='*' + tumors[each]['tumorNameEn'])[0], onto.associatedTumours,
                                 onto.search(iri='*' + a[0])[0]]
        if len(type_comment) ==0:
            return 0
        elif len(type_comment) >0:
            return 1
    for each in tumors:
        single_initial = tumors[each]
        single_final = {'content': copy.deepcopy(keys), 'pics': {}}
        for tumor_prop in single_final['content']:
            if tumor_prop in single_initial and single_initial[tumor_prop]:
                if tumor_prop == 'associatedTumours':
                    single_final['content'][tumor_prop] = [{'id': name_with_id[a[0]], 'name': a, 'type':ty(each,a)}
                                                           for a in single_initial[tumor_prop]]
                else:
                    single_final['content'][tumor_prop] = single_initial[tumor_prop]
        final_tumors_info[each] = single_final
        if 'Image' in single_initial:
            imgs = single_initial['Image']
            single_final['pics'] = {a: pd[a] for a in imgs}
    return classes, final_tumors_info


def search_name(name, type):
    result = []
    if type == 0:
        for c_id in tumors_info:
            # 对肿瘤英文名称调用find方法进行字符串匹配
            exist = tumors_info[c_id]['content']['NameInCN'][0].find(name)
            # 匹配成功
            if not exist < 0:
                # 向结果中添加id：html字符串组成的键值对
                result.append({'id': c_id, 'html': tumors_info[c_id]['content']['NameInCN'][0][:exist]
                                                   + '<span style="color: red">' + name + '</span>'
                                                   + tumors_info[c_id]['content']['NameInCN'][0][exist + len(name):]})
    else:
        for c_id in tumors_info:
            # 对肿瘤英文名称调用find方法进行字符串匹配
            exist = tumors_info[c_id]['content']['tumorNameEn'].find(name)
            # 匹配成功
            if not exist < 0:
                # 向结果中添加id：html字符串组成的键值对
                result.append({'id': c_id, 'html': tumors_info[c_id]['content']['tumorNameEn'][:exist]
                                                   + '<span style="color: red">' + name + '</span>'
                                                   + tumors_info[c_id]['content']['tumorNameEn'][exist + len(name):]})
    return result


def search_icd(icd):
    result = []
    for c_id in tumors_info:
        tumor_icd = tumors_info[c_id]['content']['ICD_OCode'][0]
        exist = tumor_icd.find(icd) if tumors_info[c_id]['content']['ICD_OCode'] else -1
        if not exist < 0:
            result.append(dict(id=c_id, html=tumors_info[c_id]['content']['tumorNameEn'] + '<br>' + tumor_icd[:exist]
                                             + '<span style="color: red">' + icd + '</span>' + tumor_icd[
                                                                                               exist + len(icd):]))
    return result


def search_mesh(mesh):
    result = []
    for c_id in tumors_info:
        tumor_mesh = tumors_info[c_id]['content']['MeshCode'][0]
        exist = tumor_mesh.find(mesh) if tumors_info[c_id]['content']['MeshCode'] else -1
        if not exist < 0:
            result.append(dict(id=c_id, html=tumors_info[c_id]['content']['tumorNameEn'] + '<br>' + tumor_mesh[
                                                                                                    :exist] + '<span style="color: red">' + mesh + '</span>' + tumor_mesh[
                                                                                                                                                               exist + len(
                                                                                                                                                                   mesh):]))
    return result


classes, tumors_info = get_all_tumors()
app = Flask(__name__)
CORS(app)
j = {'firstName': 'Foo', 'lastName': 'Bar'}
some_data = ['ahhh', 'bhh', 'cd', 'hhh']
tumors_of_brains = {}
for c_id in tumors_info:
    areas = tumors_info[c_id]['content']['hasFindingSite']
    if areas[0] != '暂缺':
        for area in areas:
            pair = {'name': tumors_info[c_id]['content']['NameInCN'][0], 'id': c_id}
            if area[0] in tumors_of_brains:
                tumors_of_brains[area[0]].append(pair)
            else:
                tumors_of_brains[area[0]] = [pair]
for c_id in tumors_info:
    areas = tumors_info[c_id]['content']['hasFindingSite']
    tumors_info[c_id]['content']['areas'] = {}
    if areas[0] != '暂缺':
        for area in areas:
            tumors_info[c_id]['content']['areas'][area[0]] = [tumor for tumor in tumors_of_brains[area[0]] if
                                                              tumor['id'] != c_id]


@app.route("/<id>", methods=['GET'])
def index(id):
    single_tumor_info = tumors_info[id]
    return jsonify(single_tumor_info)


@app.route('/search', methods=['post'])
def search():
    search_data = request.get_json()
    search_entry = search_data[0]
    search_key = search_data[1]
    print('search key: ' + search_key)
    result = []
    # 检索入口为名称
    if search_entry == '名称':
        result = search_name(search_key, 0)
    elif search_entry == 'name':
        result = search_name(search_key, 1)
    # 检索入口为ICD——O编码
    elif search_entry == 'icd':
        result = search_icd(search_key)
    # 检索入口为Mesh编码
    elif search_entry == 'mesh':
        result = search_mesh(search_key)
    # 如果没有匹配结果
    if len(result) == 0:
        result.append({'id': 'null', 'html': '无匹配项'})
    # 如果匹配项很多区前5个
    if len(result) > 5:
        result = result[:5]
    return jsonify(result)


@app.route('/tree', methods=['GET'])
def tree():
    # 前端导航栏树形组件所需要的数据
    tree_data = [[], []]
    for each in [5, 9, 20, 23, 44, 79, 148, 158, 162]:
        cid = 'tumor_child_' + str(each)
        tree_data[0].append({'id': cid, 'label': tumors_info[cid]['content']['NameInCN']})
    # 遍历每个父节点
    for p_id in classes:
        children_data = []
        for c_id in classes[p_id]['children']:
            # 单个父节点的子节点数据
            children_data.append({'id': c_id, 'label': tumors_info[c_id]['content']['NameInCN']})
        # 父节点自身以及子节点数据追加到返回列表中
        tree_data[1].append({'id': p_id, 'label': classes[p_id]['name'], 'children': children_data})
    print(tree_data)
    return jsonify(tree_data)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5200)
