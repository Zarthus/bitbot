from src import ModuleManager, utils

MSGID_TAG = "draft/msgid"
READ_TAG = "+draft/read"
DELIVERED_TAG = "+draft/delivered"

class Module(ModuleManager.BaseModule):
    @utils.hook("received.message.private")
    @utils.hook("received.notice.private")
    def privmsg(self, event):
        if MSGID_TAG in event["tags"]:
            target = event.get("channel", event["user"])
            msgid = event["tags"][MSGID_TAG]
            tags = {DELIVERED_TAG: msgid, READ_TAG: msgid}
            event["server"].send_tagmsg(target.name, tags)
