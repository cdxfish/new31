# coding: UTF-8
u"""试吃"""
from django.shortcuts import render_to_response, redirect
from django.db.models import Q
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from message.models import Msg
from new31.func import rdrRange, page, rdrtBck, f02f
from decorator import DiscussDr
import re
# Create your views here.

def applys(request):
    u"""试吃列表"""
    from models import Apply
    from forms import AppSrchFrm

    app = AppSerch(request)
    applys = app.get()
    applys = AppPur(applys, request).get()

    form = AppSrchFrm(initial=app.initial)

    return render_to_response('apply.htm', locals(), context_instance=RequestContext(request))


# @login_required
def tasting(request):
    u"""试吃表单"""
    from forms import ApplyFrm

    frm = ApplyFrm()

    return render_to_response('tasting.htm', locals(), context_instance=RequestContext(request))

def tastsave(request):
    u"""试吃提交"""
    from forms import ApplyFrm
    from models import Discuss

    frm = ApplyFrm(request.POST)
    if frm.is_valid():
        app = frm.save()
        di = Discuss()
        di.app = app
        di.save()

        messages.success(request, u'申请提交成功')

    else:
        for i in frm:
            if i.errors:
                messages.error(request, u'%s - %s' % (i.label, i.errors))

    return redirect('tasting:tasting')


def modifyApp(request, sn, s):
    u"""试吃状态修改"""
    from models import Discuss
    from purview.models import Role

    s = int(s)
    o = Discuss.objects.get(id=sn)
    _o = Discuss.objects.cStatus(sn, s)

    r = Role.objects

    return HttpResponse(Msg.objects.dumps(data={
                'sn': sn,
                'act': r.getAjaxAct(r.getActByUser(request.user, o.act[s]), sn),
                '_act': r.getAjaxAct(o.act[ o.status ], sn),
                's': _o.status,
                'sStr': _o.get_status_display(),
                'obj': 'tast'
            }
        )
    )

@DiscussDr
def notDis(request, sn, s):
    u"""试吃状态修改-> 未谈"""
    from models import Discuss
    di = Discuss.objects.get(id=sn)
    di.user = None
    di.save()
    
    return modifyApp(request=request, sn=sn, s=s)


def acceptDis(request, sn, s):
    u"""试吃状态修改-> 接洽"""
    from models import Discuss
    di = Discuss.objects.get(id=sn)
    di.user = request.user
    di.save()

    return modifyApp(request=request, sn=sn, s=s)

@DiscussDr
def refuseDis(request, sn, s):
    u"""试吃状态修改-> 拒谈"""

    return modifyApp(request=request, sn=sn, s=s)
@DiscussDr
def doneDis(request, sn, s):
    u"""试吃状态修改-> 完成"""

    return modifyApp(request=request, sn=sn, s=s)

def note(request, sn):
    u"""试吃备注填写"""
    from models import Discuss
    note = request.POST.get('note', '')
    di = Discuss.objects.get(id=sn)
    di.note = note
    di.save()

    # return HttpResponse(Msg.objects.dumps(data={
    #             'sn': sn,
    #             'note': note
    #         }
    #     )
    # )

    return rdrtBck(request)


class AppSerch(object):
    u"""
        试吃申请搜索类

    """
    def __init__(self, request):
        from models import Apply

        self.request = request

        self.oList = Apply.objects.select_related().all()

        self.initial = {
                        'c': int(request.GET.get('c', -1)),
                        't': int(request.GET.get('t', -1)),
                        's': int(request.GET.get('s', -1)),
                        'k': request.GET.get('k', '').strip(),
            }


    def search(self):
        self.oList = self.oList.filter(area__in=self.request.user.attribution_set.getAreaName()).distinct()
        
        def kSearch(k):
            self.oList = self.oList.filter(
                    Q(company__contains=k) |
                    Q(address__contains=k) |
                    Q(area__contains=k) |
                    Q(department__contains=k) |
                    Q(applicant__contains=k) |
                    Q(tel__contains=k) |
                    Q(phone__contains=k) |
                    Q(discuss__user__username__contains=k)
                )

        
        if re.match(ur'^\d{4}\-\d{2}\-\d{2}\>\d{4}\-\d{2}\-\d{2}\:(.+)$', self.initial['k']):
            d = self.initial['k'].split(':')
            dd = d[0].split('>')
            
            self.oList = self.oList.filter(addtime__range=(dd[0], dd[1]))
            kSearch(d[1])

        elif re.match(ur'^\d{4}\-\d{2}\-\d{2}$', self.initial['k']):
            self.oList = self.oList.filter(addtime__contains=self.initial['k'])
        else:
            kSearch(self.initial['k'])

        return self

    def tchcs(self):
        if self.initial['t'] >= 0:
            self.oList = self.oList.filter(time=self.initial['t'])

        return self

    def schcs(self):
        if self.initial['s'] >= 0:
            self.oList = self.oList.filter(scale=self.initial['s'])

        return self

    def chcs(self):
        if self.initial['c'] >= 0:
            self.oList = self.oList.filter(discuss__status=self.initial['c'])

        return self

    def page(self):

        return page(l=self.oList, p=int(self.request.GET.get('p', 1)))

    def get(self):

        return self.search().tchcs().schcs().chcs().page()


from purview.views import BsPur
class AppPur(BsPur):
    """
        订单列表权限加持

        获取当前角色可进行的订单操作权限.
        获取订单状态,判定可选权限.
        两者进行交集操作.

    """

    def __init__(self, oList, request):
        from models import Discuss

        super(AppPur, self).__init__(oList, request)

        self.action = Discuss.act

    def beMixed(self):
        for i in self.oList:

            if not hasattr(i,'action'):
                i.action = []
                i.sn = i.discuss.id

            for ii in self.action[i.discuss.status]:
                try:
                    if ii[2] in self.role or self.request.user.is_superuser:
                        i.action.append(ii)
                except Exception, e:
                    # raise e
                    pass

        return self
