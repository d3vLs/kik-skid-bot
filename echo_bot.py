#!/usr/bin/env python3

import logging
import sys

import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.datatypes.xmpp.errors import SignUpError, LoginError
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse, UsernameUniquenessResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse, ConnectionFailedResponse

username = sys.argv[1] if len(sys.argv) > 1 else input("Username: ")
password = sys.argv[2] if len(sys.argv) > 2 else input('Password: ')


def main():
    # set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(KikClient.log_format()))
    logger.addHandler(stream_handler)

    # create the bot
    bot = EchoBot()


class EchoBot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password)

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        self.client.request_roster()

    def on_login_ended(self, response: LoginResponse):
        print("Full name: {} {}".format(response.first_name, response.last_name))

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print("[+] '{}' says: {}".format(chat_message.from_jid, chat_message.body))
        print("[+] Replaying.")
        self.client.send_chat_message(chat_message.from_jid, "You said \"" + chat_message.body + "\"!")

    def on_message_delivered(self, response: chatting.IncomingMessageDeliveredEvent):
        print("[+] Chat message with ID {} is delivered.".format(response.message_id))

    def on_message_read(self, response: chatting.IncomingMessageReadEvent):
        print("[+] Human has read the message with ID {}.".format(response.message_id))

    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        print("[+] '{}' from group ID {} says: {}".format(chat_message.from_jid, chat_message.group_jid, chat_message.body))
        def wordMatch(sentence,word):
            global lis
            lis = sentence.split()
            if (lis.count(word) > 0):
                return True
            else:
                return False

        if chat_message.body == ("spamban") and wordMatch(sts,word="removed") == True:
            for i in range(6):
                self.client.ban_member_from_group(chat_message.group_jid, lastuser)
                self.client.unban_member_from_group(chat_message.group_jid, lastuser)
                self.client.ban_member_from_group(chat_message.group_jid, lastuser)

        if chat_message.body == ("spamban") and wordMatch(sts,word="banned") == True:
            for i in range(6):
                self.client.ban_member_from_group(chat_message.group_jid, lastuser)
                self.client.unban_member_from_group(chat_message.group_jid, lastuser)
                self.client.ban_member_from_group(chat_message.group_jid, lastuser)

        if chat_message.body == ("spamban") and wordMatch(sts,word="unbanned") == True:
            for i in range(6):
                self.client.ban_member_from_group(chat_message.group_jid, lastuser)
                self.client.unban_member_from_group(chat_message.group_jid, lastuser)
                self.client.ban_member_from_group(chat_message.group_jid, lastuser)

        if chat_message.body == ("status"):
            self.client.send_chat_message(chat_message.group_jid, "bitch stop that")

        if chat_message.body == ("Status"):
            self.client.send_chat_message(chat_message.group_jid, "What are you fucking illiterate its status not Status bitch all small just like ur brain")

        if chat_message.body == ("Spamban"):
            self.client.send_chat_message(chat_message.group_jid, "Listen pimple puss the fact you are allowed eyes is a crime itself its spamban not Spamban")


        if wordMatch(chat_message.body,word=".ban") == True:
            user_jid = lis[1]
            for i in range(6):
                self.client.ban_member_from_group(chat_message.group_jid, user_jid)
                self.client.unban_member_from_group(chat_message.group_jid, user_jid)
                self.client.ban_member_from_group(chat_message.group_jid, user_jid)


    def on_is_typing_event_received(self, response: chatting.IncomingIsTypingEvent):
        print("[+] {} is now {}typing.".format(response.from_jid, "not " if not response.is_typing else ""))

    def on_group_is_typing_event_received(self, response: chatting.IncomingGroupIsTypingEvent):
        print("[+] {} is now {}typing in group {}".format(response.from_jid, "not " if not response.is_typing else "", response.group_jid))

    def on_roster_received(self, response: FetchRosterResponse):
        print("[+] Chat partners:\n" + '\n'.join([str(member) for member in response.peers]))

    def on_friend_attribution(self, response: chatting.IncomingFriendAttribution):
        print("[+] Friend attribution request from " + response.referrer_jid)

    def on_image_received(self, image_message: chatting.IncomingImageMessage):
        print("[+] Image message was received from {}".format(image_message.from_jid))
    
    def on_peer_info_received(self, response: PeersInfoResponse):
        print("[+] Peer info: " + str(response.users))

    def on_group_status_received(self, response: chatting.IncomingGroupStatus):
        print("[+] Status message in {}: {}".format(response.group_jid, response.status))
        global lastuser,sts
        sts = str(response.status)
        lastuser = response.status_jid

    def on_group_receipts_received(self, response: chatting.IncomingGroupReceiptsEvent):
        print("[+] Received receipts in group {}: {}".format(response.group_jid, ",".join(response.receipt_ids)))

    def on_status_message_received(self, response: chatting.IncomingStatusResponse):
        print("[+] Status message from {}: {}".format(response.from_jid, response.status))

    def on_username_uniqueness_received(self, response: UsernameUniquenessResponse):
        print("Is {} a unique username? {}".format(response.username, response.unique))

    def on_sign_up_ended(self, response: RegisterResponse):
        print("[+] Registered as " + response.kik_node)

    # Error handling

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("[-] Connection failed: " + response.message)

    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

    def on_register_error(self, response: SignUpError):
        print("[-] Register error: {}".format(response.message))


if __name__ == '__main__':
    main()
