# Kent Beck Genie Sessions: Optionality (Transcript)

**날짜:** 2026년 2월 2일 (월요일)
**출처:** Kent Beck Substack Genie Sessions 라이브스트림

## 요약 (Summary)

Kent Beck이 AI(Genie)와 함께 GPU 기반의 Sorted Map 데이터 구조를 Rust와 WGPU를 사용하여 개발하는 과정의 트랜스크립트입니다. 주요 내용은 다음과 같습니다:

- **GPU Sorted Map 개발:** Get, Put, Delete(Tombstone 방식), Iterate 연산 구현.
- **Augmented Development 스킬:** 호기심(Curiosity)과 놀이 감각(Sense of Play)의 중요성 강조.
- **성장 후 분리 (Grow then Split):** 코드가 충분히 커졌을 때 추상화를 도입하고 파일을 분리하는 전략.
- **성능:** GPU를 사용했을 때 CPU 대비 Put은 3배, Get은 30배 빠른 성능(100만 요소 기준)을 보임.
- **AI와의 협업:** AI의 하위 호환성 집착이나 컨텍스트 관리의 한계를 이해하고 인간이 주도적으로 가독성을 유지하며 협업해야 함.

---

## 트랜스크립트 (Transcript)

[00:25] Okay, I think we are live
[00:29] now.
[00:31] Uh i Let's see. I should probably bring
[00:36] up.
[00:38] Let's see. Substack
[00:43] Genie sessions optionality.
[00:48] Yeah, let me uh bring this up
[00:52] on my gigantic screen
[00:55] so I can see in case it has any useful
[00:58] feedback for me, which I don't expect,
[01:00] but you know. There we go.
[01:03] Um,
[01:05] I can't see how many people are tuned
[01:08] in. I can't see any
[01:12] um
[01:13] h
[01:15] I can't see any feedback. So, you know
[01:17] what I'm going to do? I am just going to
[01:22] uh Oh, I should transition. Here we go.
[01:25] Transition
[01:27] or cut.
[01:30] Let's see. Are we doing? Yeah, we're
[01:31] doing okay. I think we're doing okay.
[01:34] [sighs]
[01:35] Um, okay. Welcome to another Genie
[01:40] session. I'm going to do some uh
[01:41] augmented development. It's a follow on
[01:44] to a session. I think it was from last
[01:46] week
[01:48] where we're building a basic data
[01:51] structure and [snorts] this time we're
[01:52] using GPUs for it. Um,
[01:57] and where we left things, I actually
[01:59] went zipping ahead
[02:02] um, and did some of this work once
[02:05] already, but uh, I want to
[02:10] let's see. I want to
[02:14] run back.
[02:17] We'll get fairy table. Okay. Okay. So,
[02:20] this is where we were. Um,
[02:26] I want to continue.
[02:29] Uh, let me see. I'm going to copy this
[02:32] commit ID
[02:35] and I'm going to tell the genie. Oh, you
[02:38] can't see my whole prompt, can you?
[02:41] What part of the screen should my mug go
[02:45] on? Probably maybe up.
[02:49] Not that one.
[02:51] this. I want to put my face up here and
[02:55] maybe even make it a little bit smaller.
[02:57] Okay,
[02:58] we'll cut to that. There we go. So, now
[03:01] you can see what I'm uh what I'm typing
[03:03] for prompt. Uh I want to roll
[03:08] back and start
[03:12] developing
[03:15] from
[03:17] this commit.
[03:20] Boom. I copied that. I paste it. I paste
[03:22] it in. And away we go. Okay. So, we're
[03:24] going to see. This is going to be weird.
[03:27] YouTube live. YouTube live. I can see
[03:31] there's this many people. They're having
[03:33] these comments live.
[03:35] Um, this thing.
[03:39] Uh, I'm probably missing something, but
[03:42] uh there you go.
[03:46] No, I'm not forcefull.
[03:50] There we go. Create a branch
[03:54] uh option called
[03:57] optionality and we'll just see where it
[04:00] goes from here. This is one of the basic
[04:03] basic skills of uh augmented development
[04:06] is throwing away stuff and doing it
[04:09] again only better this time maybe.
[04:13] So
[04:15] um so here we are. Okay. Um,
[04:22] oh, if you haven't seen this fairy tale,
[04:24] I I uh uh I recommend
[04:29] um
[04:31] reading it. This was so much fun. I just
[04:33] I hoot and hooted and hollered when I
[04:35] when I wrote this. I hope there's
[04:38] somebody listening.
[04:39] We'll find out. We will find out. Um,
[04:44] okay.
[04:47] Genie session optionality. I'm trying to
[04:50] do a million things at once. So, I'm
[04:51] looking at Substack.
[04:54] Uh, it says that it's live.
[04:58] I'm going to I'm put this in the chat.
[05:04] Start a new thread.
[05:07] Live here now.
[05:10] comment
[05:12] here for live feedback. This will all go
[05:17] out to This is only for paying
[05:19] subscribers, of course. This will all go
[05:21] out to uh
[05:24] um
[05:27] Oh, sure. Why not send it as an email?
[05:30] Um
[05:32] this will go out to YouTube later, but
[05:34] y'all can interact with me uh live right
[05:37] here right now.
[05:40] big benefits. Okay, so where was I? I
[05:42] was talking about the fairy tale.
[05:45] Uh [clears throat]
[05:46] so
[05:48] basic data structure sorted map. So we
[05:52] have four operations get, put, delete,
[05:57] and iterate between this key and that
[06:00] key. That's the sorted part of it.
[06:03] Um, I've implemented the
[06:07] uh
[06:09] I've implemented the on the CPU version
[06:12] of it a bunch of time, bunch a bunch of
[06:14] times, different languages, etc., etc.
[06:18] And the GPU gives us a completely
[06:20] different set of trade-offs. So, I
[06:22] wanted to do that. I got the basic
[06:24] operations working.
[06:27] Um, but wow, there's a bunch of GPU
[06:31] stuff that I didn't know. And here's a
[06:34] fundamental
[06:36] skill for augmented development is
[06:39] curiosity. Like, all right. All right.
[06:42] How's this working? That's one
[06:44] fundamental skill. Another fundamental
[06:46] skill [clears throat]
[06:46] of augmented development is a sense of
[06:48] play. Like, all right. Um,
[06:54] here's a goofy idea. Let's try it. If
[06:56] it's if it's reversible,
[06:59] if we can turn it around and it's not
[07:02] going to hurt anybody and it's not
[07:04] illegal and it's not immoral, just try
[07:06] it.
[07:09] The cost of short chunks of time versus
[07:13] the possibility that we might discover
[07:15] something really cool is very high.
[07:18] So
[07:21] I had to write a fairy tale that
[07:22] described how the GPU works. In the land
[07:24] of G WGPU, there lived a quiet kingdom
[07:27] called the slab. Slab kept its keys in
[07:30] perfect order, guarded by a wise keeper
[07:32] named Meta, who always knew the length
[07:34] of the realm. One day, a traveler
[07:36] brought a list of keys and asked the
[07:39] kingdom for the values. See, I I could
[07:42] write a better story than this, but I
[07:44] didn't have to. The queen. Our program
[07:46] prepared three gifts for the journey. A
[07:48] scroll of keys for the messengers to
[07:49] read. Blank ledger where answers would
[07:52] be written. That's the results buffer.
[07:53] And a tiny note telling how many keys
[07:55] there were.
[07:57] She summoned 64 sprites. Each sprite
[07:59] took one key, dashed into the slab, and
[08:01] performed a swift binary search. If the
[08:04] key was found, the sprite etched its
[08:06] value into the ledger and marked it as
[08:07] found. If not, the page was it left the
[08:09] page blank. When all the sprites
[08:10] returned, the ledger ledger was carried
[08:13] back across the boundary. That's the
[08:14] readback. And the queen scribes
[08:17] translated the markings into a list of
[08:19] answers for the traveler. And that's how
[08:21] bulk get journeys through the GPO realm.
[08:24] A scroll of keys, a band of sprites, a
[08:27] swift search, and a ledger of results.
[08:29] I'm like, okay, I understand it better.
[08:32] I don't I could still couldn't type the
[08:38] the characters to do it, but I have some
[08:41] sense. So now let's look at
[08:46] the source code. See what we have here.
[08:49] Currently everything's in one file. Now
[08:52] that doesn't mean we're going to leave
[08:53] it in one file. That just means that
[08:55] currently everything's in one file. Uh
[08:58] the principle is
[09:01] grow then split. We don't split things
[09:04] before it's time to split them. We grow
[09:06] and then we split. So, we're going to be
[09:08] doing a bunch of splitting now cuz we
[09:10] this is in the make it run, make it
[09:12] right, make it fast
[09:14] sequence. Uh we're definitely we have
[09:17] stuff running.
[09:19] We need to make things right.
[09:23] So,
[09:24] we have this sorted map. It has all
[09:27] these buffers.
[09:30] Uh
[09:32] and then
[09:35] we have compute pipelines
[09:38] forget the get bind group the where's
[09:43] the merge merge bind group.
[09:47] Okay. So there's still stuff I don't
[09:49] understand. That's fine.
[09:53] Um
[09:54] and then a bin. So,
[09:58] we'll let's just scroll through all of
[10:00] the code and have a quick look at it.
[10:02] Doesn't mean we'll understand it, but
[10:03] we'll understand kind of what's going
[10:06] on. So, there's a new that just
[10:08] initializes all this stuff.
[10:11] Um,
[10:15] bulk get
[10:19] uh bulk get pipeline. Bulk merge.
[10:25] Bulk merge pipeline.
[10:29] Uh, get put. Oh, and have we not
[10:32] implemented delete yet? I I I told you I
[10:34] scrolled back. bulk put
[10:38] which is this big long complicated
[10:40] thing.
[10:42] bulk get
[10:45] again big long complicated thing
[10:49] and maybe we haven't implemented delete
[10:51] so we have to implement delete again
[10:52] okay so
[10:55] uh implement
[10:57] delete
[11:02] and bulk
[11:05] delete
[11:07] by storing a
[11:10] tombstone stone
[11:15] write tests for it [clears throat]
[11:19] and all corner cases. There we go.
[11:27] So, we had a little bit more work to do.
[11:31] That's okay.
[11:33] Uh threw away some work, but you know
[11:35] what? When work is cheap, then we can
[11:38] throw it away. Hey, I have a reply to my
[11:40] chat. Those watching the stream can join
[11:43] a live chat by clicking the eye icon I
[11:46] icon in the upper right corner. But can
[11:49] I do that?
[11:52] Where is the live chat? Okay, Metam
[11:55] Monkey Metal Metal,
[11:59] I'm [clears throat] terribly sorry for
[12:00] mispronouncing your name.
[12:04] Metal monkey.
[12:06] Um, yeah.
[12:09] I'm not
[12:11] seeing how I can do that, but that's
[12:13] okay.
[12:14] Um,
[12:16] if you know, post a comment on my chat
[12:20] and then we'll go from there.
[12:23] We now know at least one person is
[12:27] watching, so that part's good.
[12:30] Um,
[12:34] okay. Here we go. Added tombstone back
[12:36] delete bulk delete updated GPU bulk get
[12:38] shader to treat tombstones as missing
[12:41] and covered corners in corner cases and
[12:44] tests
[12:50] existing key delete mixed keys
[12:52] duplicates delete then put and empty
[12:55] bulk delete want me to oh run no don't
[12:58] bother running the tests okay when I say
[13:04] bazinga
[13:07] run tests.
[13:10] If they all pass, run Perf and store
[13:16] results because Perf is important.
[13:20] Uh then commit
[13:24] and push.
[13:30] Bazinga. There we go.
[13:34] Even that amount of I'm helping
[13:38] 17 live viewers now media conglomerate
[13:42] cannot be far behind. So here we go. Um
[13:46] where are you seeing this? I am not
[13:48] seeing this and I wish I was but that's
[13:50] okay. If somebody can tell me how to
[13:53] find it. I've done YouTube lives before
[13:55] but I've never done a Substack live
[13:58] before.
[14:00] I would be happy to see it. But here we
[14:03] go. Um, I wonder if I just click on the
[14:07] live video. Do I do I just be go into a
[14:11] recursive hell? Okay. Um, I want this.
[14:22] Okay. So, we're we can't even run the
[14:25] tests.
[14:30] In our view, the count is right above my
[14:33] face. Okay. Well, in my I don't have a
[14:36] view, but okay.
[14:38] Welcome 17 paying subscribers. Great to
[14:43] have you here.
[14:45] Oh my goodness. We're installing a bunch
[14:48] of stuff, but that's what one does. At
[14:50] least I don't have to install it.
[14:53] We'll see how this goes. So the plan
[14:55] here is to go for about 45 more minutes.
[14:59] Now cargo test please run
[15:06] profiling foreign types. Wow. Okay.
[15:11] Well, it's doing a lot of stuff. I hope
[15:14] it's doing the right things. Um 45
[15:16] minutes. Um, if you want to ask me
[15:20] questions, I guess you can do it on on
[15:23] the uh chat thread.
[15:25] Um,
[15:29] okay.
[15:32] We're going to run the Perf because
[15:34] we're going to keep track of like
[15:36] performance versus uh CPU
[15:41] is important.
[15:43] Someday I'll get a real gigantic
[15:47] um
[15:50] Nvidia machine with Nvidia on it and
[15:54] we'll see how this goes when we're
[15:55] really
[15:58] when we when we're really pushing it. Um
[16:01] but that'll be later. Test passed. Perf
[16:03] ran and stored. Committed and pushed
[16:05] optionality. There we go.
[16:08] No, no, no PR. We're just going to stack
[16:11] up a bunch of commits here. Okay. So,
[16:16] um let's see
[16:22] what's what do I want to do next? Okay.
[16:25] So, we've got a bunch of duplication. We
[16:27] have bulget get put. This is all.
[16:33] Okay. So, this
[16:38] bulk put is this complicated thing. bulk
[16:41] get is this complicated thing. Okay.
[16:44] So,
[16:50] um let's explore some more structures.
[16:54] We have these three operations bulp put,
[16:57] bulk get, bolt delete that have all this
[17:00] WGPU stuff in them and they look quite
[17:03] similar. We'll just we'll just scroll
[17:06] and have a look at it. Um, by the way,
[17:10] how's the um
[17:12] how's the readability of the text here?
[17:15] I have had people complain about that
[17:18] before.
[17:19] So, bulk get looks like it grew quite a
[17:23] bit before you split. That's okay. Um,
[17:26] here's the thing,
[17:29] Marco. Thanks for the question. Uh
[17:34] yeah, it's okay if you know if you know
[17:37] what the structure two things, two
[17:39] reasons to pull a a a piece a structure
[17:44] decision sooner.
[17:46] If you know what the structure should
[17:49] be, for sure, for sure. And it's not
[17:52] going to delay you too much to introduce
[17:55] the structure now, then sure, pull it
[17:57] in.
[17:59] I've never done this is not true. I
[18:02] haven't done GPU programming for 20 25
[18:06] years. So I don't know what the
[18:09] structure should be. Uh the this WGPU
[18:14] API is [clears throat] so complicated.
[18:18] It's got so much detail and and no
[18:21] abstractions. This is a pure lumper API.
[18:26] Um, did I talk about lumpers and
[18:29] splitters and tidy first? Uh, so anyway,
[18:32] someplace in there, uh, lumpers and
[18:35] splitters. Lumpers like to have big
[18:38] elements so they can see everything all
[18:40] in one place. And splitters like to to
[18:44] have lots of little things that compose
[18:46] together to to cause to create
[18:48] solutions. This is a classic lumper API.
[18:52] all the flexibility. But as you can see,
[18:56] when I go to implement this get
[18:58] operation,
[19:00] I create a buffer.
[19:03] I create the results buffer and the
[19:05] readback buffer. And how's that
[19:07] different from the results buffer? We
[19:08] don't know yet. And then there's a meta
[19:10] buffer. And then we have a bind group,
[19:13] whatever that is. And then we have bind
[19:15] group entries. And then we've got an
[19:18] encoder. And then a pipeline. And then
[19:22] we copy some stuff and then with the
[19:24] results and then so somewhere in here we
[19:27] actually must
[19:30] execute some code on the GPU but it's
[19:33] not at all clear where it is.
[19:36] So um for the three bulk
[19:43] operations
[19:46] there's lots of duplication
[19:51] create a strct for each. If so we if I
[19:55] was in an object-oriented language I'
[19:57] I'd use an object but that's okay.
[20:02] um
[20:04] that
[20:08] captures
[20:10] the commonality.
[20:12] Um Marco,
[20:15] um you're you're absolutely right to
[20:18] question what time do you make these
[20:20] changes? And that is part of the design
[20:24] skill.
[20:26] Um, [clears throat] by the way, if
[20:28] anybody says something really
[20:30] interesting in the live chat, wherever
[20:32] that is, please let me know. And if you
[20:35] can tell me how to get to the live chat,
[20:37] please let me know about that, too, cuz
[20:39] that would be useful. I'd be even more
[20:42] distracted than than I am now, which is
[20:45] pretty damn distracted. Did I tell you
[20:47] this is a this is a cussing
[20:51] uh channel?
[20:56] Oh, Marco. Sure. Okay. So, Marco, here's
[20:59] the question. If you have never done
[21:03] GPU stuff, you don't know Rust. How many
[21:06] structured decisions do you want to
[21:08] make? As few as possible. Let's get
[21:11] something working. This is the classic
[21:13] make it run, make it right distinction.
[21:15] Let's get something working
[21:18] and then we can talk about the structure
[21:20] that we should have had. So, I look at
[21:23] this API, this WGPU API with all of its
[21:29] whatever entries and blah blah blah, and
[21:31] I just think, boy, there's missing
[21:33] abstractions here. 100% missing
[21:36] abstractions here. So,
[21:39] I don't know what they are yet, though.
[21:41] But we have some examples from which we
[21:44] can
[21:46] uh generalize.
[21:54] Okay. Equals
[21:57] bulk merge pipeline.
[22:00] Okay.
[22:07] Now delegate to their respective strcts.
[22:09] Added create uniform buffer to
[22:11] centralize uniform buffer creation.
[22:13] Well, thank you for that. Added bulk put
[22:16] op, bulk get op, and bulk delete
[22:18] opstrurs.
[22:20] to hold operation specific state and
[22:22] execution. Okay. Refactor the three bulk
[22:25] operations into dedicated strcts. So the
[22:28] shared setup dispatch readback logic is
[22:30] encapsulated per operation with a small
[22:32] uniform buffer helper to reduce boiler
[22:36] plate. Okay. Yeah. Bazinga.
[22:44] Oops.
[22:45] I like it that I don't have to worry
[22:47] about typos so much with the genie. My
[22:50] compiler has never been this forgiving.
[22:52] Oh my goodness. What was I doing
[22:54] yesterday? Oh, I was adding a contact
[22:58] on my iPhone, you know, and you have to
[23:00] there's first name, last name, phone
[23:03] number, and I just copied some text.
[23:08] And I just wanted I'm so used to the
[23:11] genie now. I just wanted to say add this
[23:14] context here's some text and it would
[23:16] just do it and instead I had to go
[23:21] I had to go like copy the name first
[23:24] name and paste it into the field and
[23:26] second ah ah
[23:29] absolutely crazy. Okay.
[23:36] All right. I think we're I think we're
[23:39] we're good
[23:41] now. Bulk get bind group layout.
[23:46] This stuff should be inside the strct.
[23:51] That was the whole point.
[23:56] Where are we?
[23:58] Okay. [clears throat]
[24:06] All right, let's have a look at where we
[24:09] are. Okay, now seems like these ops
[24:15] put uh put the opstruct
[24:21] into an operations.
[24:25] RS.
[24:27] Do we want to do we we definitely want
[24:29] to do this, but the question is when do
[24:32] we want to do it? Um, I'm tempted to do
[24:35] it right now, but
[24:38] I'm not sure.
[24:41] Um,
[24:43] bulk get up, bulk put up. Somebody's
[24:48] messaging me. Hi, person.
[24:52] Uh, GPU sorted map. Okay, here we have
[24:54] new.
[24:57] Let's look and see if this looks start
[25:00] is starting to look simpler. slab size,
[25:03] slab capacity, input buffer,
[25:06] slab metadata,
[25:08] metabuffer,
[25:12] merge buffer.
[25:14] Okay. So
[25:17] um for the put operation so the way put
[25:22] works
[25:27] do all the computation possible
[25:35] on the GPU.
[25:40] So this merge buffer stuff I think is
[25:43] related
[25:45] bulk get shader that belongs in the get
[25:48] op.
[25:53] Okay.
[25:56] Plan the next moves. We'll see what it
[25:57] does.
[25:59] Um [snorts]
[26:01] I'm probably going to spend two hours on
[26:05] this. I spent an hour getting something
[26:07] to work and I'm probably going to spend
[26:08] two hours on the make it right part.
[26:15] What do you want moved? Sort and
[26:17] dduplicate. Yeah.
[26:23] A
[26:27] here we go.
[26:29] GPU
[26:31] GPU sort and ddup incoming.
[26:38] uh al sort ddup. Okay. So the way put
[26:43] works is we we have the slab itself the
[26:48] the on the GPU we have the sorted
[26:51] entries. We're going to have a bunch
[26:53] this is bulk put. So we're going to have
[26:55] a bunch of new entries. We need to sort
[26:57] them so that we can merge them in. We
[27:00] need to dduplicate them. If we have uh
[27:03] duplicate
[27:05] um entries, we have to decide what what
[27:08] the expected behavior is. If we're
[27:10] putting two different values in the same
[27:12] bulk put, I think probably just
[27:17] blow up. So, we'll think about that in a
[27:19] minute. All possible step capacity check
[27:22] right back meta. Let's see.
[27:35] Oh,
[27:38] here. See?
[27:41] Uh,
[27:43] create sort. Why not?
[27:47] Okay, I needed to click instead of
[27:49] typing. Okay, fine. UI for these things.
[27:54] Boy, an IDE is the wrong
[27:58] absolutely the wrong
[28:00] tool for this kind of thing. Update.
[28:10] Yeah. Go.
[28:20] All right.
[28:21] All right. Now, we'll see. So, one of
[28:23] the nice things about using a genie is
[28:25] you got time to talk. You've got these
[28:29] two minute, three minute, five minute
[28:31] kind of moments. And uh I love pairing
[28:37] plus a genie cuz you just have plenty of
[28:40] time to roll back and go h of coffee.
[28:45] What are we going to do? And
[28:48] there's a real progress being made.
[28:50] There's a big difference between that.
[28:52] Woo!
[28:54] I need more c Speaking of more coffee.
[28:56] Uh, hope you've all got plenty of
[28:58] caffeine here. Um, welcome y'all. Thank
[29:02] you so much for tuning in. Even though I
[29:04] can't see you and I don't know
[29:07] if people are here, how many people are
[29:09] here, that'll I can live with that. Um,
[29:12] I'm just going to talk to myself. I
[29:15] honestly talk to myself pretty much all
[29:17] day every day anyway. So, there we go.
[29:21] Um,
[29:26] where was I? Oh,
[29:29] [snorts] yeah.
[29:32] I don't have a deficit of attention.
[29:34] Let's just be clear. I'm just extremely
[29:37] sensitive to boredom. As soon as
[29:40] something gets boring, my brain just
[29:42] goes someplace else. So, I call it
[29:43] boredom sensitivity.
[29:46] Um planning next moves
[29:55] GitHub repository setup but I don't know
[29:58] what that is all about but here we are
[30:02] map what is
[30:10] huh [clears throat]
[30:11] yeah well uh I'll interrupt it in a
[30:14] minute as soon as I run out of random
[30:17] thoughts
[30:18] to spew out.
[30:21] So
[30:24] it's so tempting, you know, we've got
[30:27] here we have these operations here. We
[30:29] have a data structure, we have some
[30:30] operations, we finished one operation,
[30:32] we just want to jump to the next one.
[30:35] and
[30:39] noticing that there's a gap in there
[30:42] where we can improve optionality
[30:45] by in this case we're pulling these
[30:47] operations out into separate
[30:51] scopes. We'll call them scopes, okay?
[30:54] Um these optructs
[30:59] and they're not going to they're they're
[31:01] going to be similar to each other. So
[31:03] we'll look for chances to further pull
[31:06] out uh
[31:10] chunks.
[31:12] Um but first we have to get everything
[31:16] out of
[31:18] that um
[31:21] the the the the GPU sorted map and into
[31:25] these operation strcts. And then once we
[31:28] do that, then we can look for further
[31:31] abstractions that are going to help us.
[31:34] Um, as I said, I spent 29 live viewers.
[31:38] If you want to spend a minute explaining
[31:39] how your agents are running and the
[31:41] guardrails you put up to protect your
[31:43] code, it would help catch up those of us
[31:45] that missed the first session. Okay. Uh,
[31:49] this is a live coding, a live streaming
[31:53] coding thing that I have not picked up
[31:56] yet, which in the radio world they
[31:58] called a reset.
[32:01] And we're back. We're talking to blah
[32:04] blah blah blah blah. So,
[32:07] the current uh operation 29 live
[32:09] viewers. I think that's a record for me.
[32:11] And that's just paying subscribers. Only
[32:14] paying subscribers get to watch this
[32:16] live. it'll go up on YouTube and then
[32:18] it'll be a dead video and people can
[32:20] comment on say all the nasty things they
[32:22] want to
[32:24] um but here you are. Thanks so much. The
[32:28] reset
[32:29] the pro the problem we're solving. So
[32:32] it's called the genie sessions. It's me
[32:34] coding with a genie who's which
[32:36] currently looks like it's in some kind
[32:38] of infinite loop. Um
[32:42] but uh
[32:44] we we'll we'll interrupt that. So,
[32:46] [clears throat] Genie sessions, we're
[32:48] coding with a genie. The problem we're
[32:49] solving is a sorted map where we're
[32:53] storing the entries on the GPU. And on
[32:57] the GPU is where we're going to do
[33:00] updates.
[33:01] The [snorts] there's four operations.
[33:04] Get, put, delete, and iterate from
[33:09] [clears throat] element from key to key.
[33:13] So, those are the four operations. I
[33:15] spent an hour last week getting the
[33:17] basics running [clears throat] and uh
[33:21] now we've spent half an hour on the
[33:24] structure but the genie appears to be
[33:26] locked up. Okay. Uh,
[33:30] are you stuck
[33:42] edit cute message?
[33:47] Okay, so I'm just gonna quit this
[33:55] GitHub.
[34:00] The word
[34:04] claims to be planning the next move, but
[34:06] was it really
[34:11] complex and large? Exploring existing
[34:13] shaders in the code is needed to find
[34:16] reusable GPU sorting parts or plan a
[34:19] simplified GPU plot since G CPU sorting
[34:23] is explicitly disallowed. Yeah. Oh,
[34:26] you're trying to make this easy on
[34:27] yourself. I'm not interested in making
[34:29] it easy on you. I'm interested in you
[34:31] making it easy on me.
[34:34] Okay. Uh Sean, I hope that was the reset
[34:36] you were looking for.
[34:39] Um,
[34:42] boy, it's thinking hard.
[34:49] Yeah, I would like I would like uh more
[34:51] updates. Perfect. Thank you. You're very
[34:54] welcome.
[34:55] This is fun. This is ah [sighs]
[35:01] I had a a beautiful critique
[35:06] by uh Ron Jeff, my old old friend.
[35:10] We've been friends a long time. Plus,
[35:12] he's really old, but that's a separate
[35:14] issue.
[35:16] um about coding with the genie and being
[35:20] worried about the climate effects of it,
[35:22] being worried about the concentration of
[35:24] power effects of it. Um and I get all
[35:28] that and I think the most effective path
[35:33] forward is
[35:36] to engage with it. my stage of life, my
[35:39] stage of career. Um, so
[35:45] earlier you were considering moving
[35:46] operations to their own module. What
[35:48] would be the downside? Um,
[35:51] ah, if Okay, so current state here's
[35:56] where I want to be able to just scribble
[35:58] a a picture, but okay.
[36:03] You should have a window like this. Uh,
[36:06] metal monkey. Where's the I
[36:10] [clears throat]
[36:13] I'm not getting I'll sort that out
[36:16] later. Maybe I'll have a practice
[36:18] session and you can show me how to do do
[36:20] this better. [snorts] Um,
[36:24] okay. Where was I? Uh,
[36:28] moving operations to their own module.
[36:30] Okay. So, if we have things in one file
[36:32] and we need to move stuff around, that's
[36:34] relatively easy.
[36:36] If we move the operations
[36:39] to their own file and then we have to
[36:41] move stuff between them, that's harder.
[36:44] So if I'm going to move stuff into the
[36:46] operations as I am with this put
[36:48] operation, I want to leave things still
[36:51] in one. I don't mind if the elements get
[36:54] kind of uncomfortably big. And I use the
[36:57] analogy with biology here. the cell gets
[37:01] bigger and bigger and it starts to get
[37:03] kind of stretchy and then it separates.
[37:05] That's when it separates. It doesn't you
[37:07] don't you don't sit there and build a
[37:10] factory for cells and you make little
[37:12] tiny ones and make each of them bigger
[37:14] and bigger and bigger. No, you have one
[37:16] thing. It gets
[37:19] big and then splits. So, that's what I
[37:21] want to do. And and practically here I
[37:24] don't want to have to do a bunch of
[37:27] motion between files if I can help it.
[37:31] If I have to then fine whatever.
[37:34] Planning a staged put bulk put oper
[37:37] factor by introducing GPU sorting
[37:39] scaffolding with rated space
[37:42] new structured prams and reorganized
[37:45] buffers for input sorting scanning DDUP
[37:48] and scattering while still supporting
[37:51] CPU fallback. Initially I don't want no
[37:53] don't
[37:56] no CPU fallback
[38:01] if WGPU
[38:03] is not available.
[38:07] Abort.
[38:10] Okay. So that's queued up. All right.
[38:13] Boy, if this passes I will be
[38:18] surprised and delighted.
[38:20] But that's it.
[38:22] >> [sighs]
[38:23] >> Is is it harder for Pete asks hello
[38:27] Pete? Uh is it hard for the genie
[38:30] though? Yes, it is harder for the genie.
[38:31] It expands the context window. It
[38:33] increases the chance that
[38:36] um it's going to make a mistake that
[38:39] it'll get stuck.
[38:41] Um,
[38:44] okay. Here we are.
[38:49] Drafting a new large WGSL shader string
[38:52] for bulk put. [sighs]
[38:55] See that lib RS? We didn't even scroll
[38:58] far enough to see the GPU code, the
[39:02] source code for the GPU down there.
[39:05] Philip, hey, Kent, your legend. I don't
[39:07] know. Didn't know the session, but I had
[39:09] to click on I have to go. Got to book
[39:12] the show. Enjoy your show, Phillip. Have
[39:14] a great weekend.
[39:16] Uh,
[39:18] only overindulge if you're safe. There
[39:21] we go. That's my advice.
[39:24] Um, where can we read from Ron Jess now?
[39:28] Still active on his blog. I don't know
[39:29] about it on his blog. The the uh
[39:31] question Ron had was on Oh, that's what
[39:35] I was doing. That's what I was talking
[39:37] about. The question. This is a great
[39:40] place if you have boredom sensitivity
[39:43] like I do cuz we are all like that. If
[39:46] you want a single cohesive coherent
[39:49] thread start to finish
[39:52] not the place for you. Um Ron's comment
[40:06] was on
[40:00] an earlier chat thread I think. Um maybe
[40:05] somebody can help you out with that. Uh,
[40:08] I'm still waiting, hoping,
[40:13] praying
[40:15] that the genie is going to give me some
[40:17] code that works in
[40:22] that and and it'll be all uh inside
[40:25] inside these smaller scopes. Okay. So
[40:30] when I notice this duplication between
[40:32] the operations
[40:36] there's bunch of paths forward I can
[40:38] imagine. So what I'm doing though is
[40:41] creating a scope for each operation and
[40:44] then I expect there to be considerable
[40:46] duplication between them where we set up
[40:50] a thing and set up set some buffers some
[40:53] memory and then we set up some
[40:55] operations and then um and we use them.
[40:59] Oh, and I'm using Cursor. Cursor is not
[41:02] a paying uh sponsor of the show. Not
[41:05] yet.
[41:06] Um, if you know somebody who would be
[41:09] interested in sponsoring these, uh,
[41:12] Genie sessions, please do send them my
[41:15] way. Um, this is also how I make my
[41:18] living. Ah, which is part of my response
[41:21] to Ron Jeff.
[41:23] And he's retired and doesn't need
[41:26] income. And that's great and fantastic.
[41:28] And I'm so happy he did the work. He's
[41:31] getting the rewards. Um, part of my
[41:35] motivations is that I do need to still
[41:39] make a living and pay for my house and
[41:41] stuff. [sighs and gasps]
[41:43] So, that is definitely part of it. And I
[41:45] don't want to pretend that it's not I'm
[41:46] not doing this for the good of humanity.
[41:49] I am doing it for my fellow geeks to
[41:52] help geeks feel safe in the world. Uh,
[41:55] oh, you can't derail me, Philip, because
[41:57] there's no rail. Um,
[42:02] also though I do it because I just love
[42:05] this stuff. Just being in this
[42:09] I have all this code and it's really
[42:12] complicated and I don't understand but I
[42:14] have to make progress. Ah,
[42:17] this is I'm in hog heaven.
[42:20] Absolutely. This is
[42:23] I'm exercising muscles and honestly I'd
[42:26] just gotten fed up with excuse my nose.
[42:30] [snorts] I'd gotten fed up with all the
[42:35] hassles of
[42:37] of doing any kind of programming
[42:42] and now I get to exercise.
[42:45] [laughter]
[42:48] Thank you, Pete. That's a That is a
[42:50] t-shirt. Rude 2008 Ruby on Rails 2026
[42:55] Kent off Rails.
[42:57] Um
[43:01] where where was I? Okay. Okay. So, why
[43:04] am I doing this? Uh one, cuz I got to
[43:08] make a living. Two,
[43:10] because I really enjoy it. Three,
[43:14] everybody is panicked about augmented
[43:19] development
[43:20] and people react to that panic in many
[43:23] different ways. There are the the
[43:26] unthinking cheerleaders and I was a
[43:29] cheerleader so I know what how that
[43:31] goes.
[43:34] Um,
[43:37] there are the unthinking critics.
[43:42] You know, I'm just never going to touch
[43:44] one of those things. And and even quite
[43:47] emotional about it, like this is a moral
[43:50] stance and if you touch a large language
[43:54] model, then you're evil and horrible and
[43:56] blah blah blah. And that I don't think
[43:59] that's helpful. Um, a lot of people in
[44:02] between, a lot of people dipping their
[44:04] toes, a lot of people not ready to dip
[44:07] their toes.
[44:11] Uh, wisdom. Phillip. Philip asks for
[44:13] wisdom about AI. And that's a tall tall
[44:16] order at this point. Um, but it's not
[44:20] for me to judge. I'm just doing my thing
[44:22] and I'm doing it in public the way I've
[44:24] been doing it for the last
[44:27] for years.
[44:29] Okay. Get input operations including
[44:31] bind group layouts and buffers sorting
[44:33] delocated and buffer usage after rating
[44:35] sorts are confirmed correct ensuring
[44:39] the compact buffer is preserved for
[44:42] merging. Okay, cool cool.
[44:45] Um,
[44:48] so it claims to have done this stuff.
[44:54] Where is it in its thinking? cuz this is
[44:57] weird that it I can see these
[45:00] todos and there's spinny things here. I
[45:03] can see spinny things. I don't know if
[45:04] you can. And there's some GitHub
[45:06] repository setup and I don't know what
[45:08] that is for. Um, okay. So, it's still
[45:12] it's still doing it. Okay. My people, us
[45:17] geeks are panicked and my mission is to
[45:20] help geeks feel safe in the world. And
[45:23] we can go into that sometime. You look
[45:25] in my about on Substack and you see it.
[45:29] Um I and so
[45:33] pay my bills cuz [clears throat] I love
[45:35] it
[45:37] and because it is a service to my
[45:40] community.
[45:42] Um I think these are incredibly powerful
[45:45] tools.
[45:47] They are going to affect our lives
[45:50] whether we use them or not. They're
[45:51] going to affect our professional lives.
[45:54] Uh, we have a lot to lose. We also have
[45:57] potentially a lot to gain.
[46:00] Assessing buffer bindings and scan add
[46:02] dispatch. Usually, it does not take this
[46:05] long.
[46:08] I'm tempted to just roll this back. We
[46:10] have 15 minutes to go and I want to see
[46:12] some progress.
[46:14] So, this was too big a chunk. Hm. So, I
[46:18] made that decision earlier. had asked me
[46:20] about
[46:22] um
[46:25] uh whether to use a simpler sort radic
[46:29] sort
[46:31] whatever whatever um maybe I'll give it
[46:33] another two three minutes and then I'm
[46:35] just going to roll back
[46:39] test will not run but could be triggered
[46:45] run.
[46:48] Oh, all right. So, still says it's
[46:51] thinking.
[46:54] Okay.
[46:58] Okay. So now it's now
[47:02] this the genie is obsessed with
[47:06] backwards compatibility
[47:08] and it's just it's willing to add so
[47:11] much
[47:13] complexity
[47:15] to maintain backwards compatibility for
[47:17] code that no one else is calling.
[47:21] And I think this is a symptom of having
[47:24] looked at just a whole bunch of repos on
[47:28] GitHub that have a bunch of backwards
[47:30] compatibility stuff in there, but it
[47:33] doesn't doesn't have a concept of why
[47:36] backwards compatibility is useful or
[47:38] when it's useful or when you don't want
[47:40] it. And it's willing to blow so much
[47:44] complexity just to make it. Added a
[47:46] hardboard. Okay, cool. B. Here we go.
[47:52] Don't tell me to bazinga. You bazinga.
[47:55] There we go.
[47:57] And I love doing these kind of little
[48:00] tuning of my
[48:04] Now, why I can't run cargo tests? Some
[48:06] somebody tell me run this time only. How
[48:09] about run it every time?
[48:12] But that's okay. Uhoh. Had problems. But
[48:16] it will fix it. That's the nice thing.
[48:22] Uh, I'm now running. No,
[48:29] running
[48:30] test. Here we go. Phillip, till next
[48:33] time. You You rock.
[48:39] Now we'll run cargo test.
[48:44] Success.
[48:46] And then we're gonna remember how fast
[48:48] things are.
[48:52] Oh, something failed.
[49:02] Oh, thanks so much for tuning in. We are
[49:06] using a genie to um to comp to implement
[49:12] a uh basic data structure a sorted map.
[49:17] We have uh three operations
[49:20] are we do need to add that fourth
[49:23] operation. We need to add the uh
[49:24] iteration
[49:26] between from key to key.
[49:32] No. What went wrong? Get diff. Okay.
[49:38] Get log
[49:43] create mode get push.
[49:46] All right. So uh the uh repo is uh
[49:52] kentback slashgpu
[49:54] sorted map and we're on the optionality
[49:58] branch. Test improve committed and
[50:00] pushed.
[50:02] Okay. Okay. If you want a PR opened, say
[50:04] the word. I don't want a PR open. No.
[50:06] Okay. So, let's have a look at where we
[50:10] are. Oh, so we want uh we had an earlier
[50:13] question about what point do we put
[50:15] these ops these operations in their own
[50:18] file. It's when everything possible has
[50:22] been moved
[50:25] from
[50:27] Okay. Okay. So, let me just I'll just
[50:28] ask is
[50:31] uh everything
[50:35] possible moved
[50:40] into the opstruct
[50:46] so we can extract
[50:49] an ops. RS
[50:53] helper file. There we go.
[50:58] No question mark.
[51:01] Just as I was saying it, I my voice. Is
[51:04] this true? We'll find out.
[51:07] 10 minutes ago. Uh, wow. Thank you all
[51:11] so much for tuning in. You know, I I do
[51:16] this even if nobody's watching, although
[51:18] I'll do it with the people watching to a
[51:21] greater degree.
[51:22] Um well apparently it was happy
[51:28] this per planning ops rs refactor okay
[51:31] exploring I'm preparing to inspect the
[51:33] file to decide if the helper function
[51:36] okay [snorts] so why extract out pieces
[51:42] this is just a guess I'm guessing from
[51:44] what I see of the external behavior if I
[51:46] have a single file and it gets too long
[51:50] then the gene genie doesn't get the
[51:53] right context to make changes.
[51:56] If I break it out into multiple files
[51:58] and importantly the genie only has to
[52:02] operate on a single file at a time then
[52:06] it seems to operate much better.
[52:10] If I break it out into two files and now
[52:12] the genie has to make some change that
[52:16] spans two files then it gets stupid
[52:18] again.
[52:20] So, I might want to merge
[52:23] back in temporarily and then extract
[52:26] again.
[52:27] Um, eventually the genie will figure out
[52:30] how to do this for itself, but it is not
[52:33] good at this yet. I'm better at it than
[52:36] it is, and you are better at it than it
[52:38] is, too. So,
[52:41] yeah, we're getting rid of a bunch of uh
[52:45] stuff in the the lib RS file, the basic
[52:49] one.
[52:51] Um,
[52:58] and we have an ops RS file that's
[53:00] getting longer and longer as it should.
[53:04] And now we can The thing I like about
[53:07] this, this is so this is an example of I
[53:10] haven't
[53:12] removed any coupling. I haven't removed
[53:15] any complexity. I haven't removed any
[53:17] duplication. But I've created
[53:20] a co a more cohesive environment if all
[53:25] that's in this ops. RS file is the three
[53:27] ops.
[53:30] Uh and there's an opportunity to
[53:32] simplify here. Bind group entries. Like
[53:36] I there's something going on here that's
[53:38] really the same between all three.
[53:42] Oh, uh helpful tip. I have an enormous
[53:46] screen. You absolutely should have an
[53:49] enormous screen. I can't show you
[53:52] a third of the vertical
[53:56] uh that I use when I'm
[54:00] actually coding by myself or coding with
[54:02] a pair. Um,
[54:06] having a bunch of vertical
[54:10] uh pixels is really really helpful for
[54:13] this kind of stuff cuz I want to see a
[54:15] bunch of things at once to see what I
[54:17] can pull out.
[54:20] Um, okay.
[54:27] Shader sources and pipeline. Okay. So,
[54:30] uh, bazinga
[54:37] then put the shader
[54:40] sources
[54:42] in ops.
[54:45] Here we go.
[54:48] Sean says, "An ne suggested the neuron
[54:52] the other day
[54:55] to have the genie generate a new file.
[54:57] contains a map of files and functions
[54:58] with generated explanations of each.
[55:00] Then you can set your system prompt to
[55:02] have agents consult the first the file
[55:05] that file first to reduce token usage
[55:08] and context bloat. Yeah. Yeah. Yeah. So
[55:12] let's try that
[55:17] next. This is like a index a table of
[55:20] contents.
[55:22] Okay.
[55:30] And we're going to store some
[55:31] performance.
[55:34] Oh, we should ask how the performance is
[55:36] trending
[55:39] for large data sets.
[55:50] Now is performance
[55:54] trending for large
[55:58] data sets.
[56:02] Oh, what did it do?
[56:05] It's uh subtracting looks like GPU code
[56:11] from lib RS. Good. Good.
[56:14] Good. Because like lib RS is our entry point.
[56:17] That's that's the that's the beginning
[56:20] of the navigation. We don't need
[56:23] actually much that's really GPU related
[56:27] there.
[56:32] this this bulk get op is going to
[56:36] uh
[56:39] is going to invoke some GPU code and
[56:42] we'd like that GPU code to be close to
[56:45] the operation that invokes it because if
[56:47] I change one I'm going to have to change
[56:49] the other classic uh tidy first
[56:53] coup uh cohesion and coupling
[57:00] Yeah,
[57:07] good, good, good, good. I mean, good. If
[57:10] it works,
[57:11] this is what I was expecting to see. uh
[57:15] you know and I
[57:17] I don't know all this stuff but we can
[57:21] figure out any part of it that we need
[57:23] to figure out. That's the key
[57:27] cuz we are geeks.
[57:36] I Why did Why is that running? Okay.
[57:40] Bazing half. We were halfway through.
[57:51] Bazinga.
[57:53] Just have a couple of
[57:55] Oh, let's see if it can parse that. Um,
[57:59] just a couple minutes left in our genie
[58:02] session. Uh, thank you all for tuning
[58:05] in. Those of you who did tune in, those
[58:07] who didn't tune in, we could say any
[58:09] nasty thing about you that we want
[58:11] because you're not tuned in. You'd have
[58:13] to wait to see it.
[58:16] Um, Mike asks, "I can see a potential
[58:19] argument that AI has a different ability
[58:21] to read code than a human, so maybe we
[58:23] don't need to tidy it in the same way.
[58:25] Are we still writing code for humans to
[58:27] read? I assume. Are we thinking in terms
[58:29] of writing code for an AI to read?
[58:33] >> [sighs]
[58:38] >> thought experiment. What if we came up
[58:40] with a programming language that was
[58:42] fantastic for LLMs to manipulate and
[58:45] impossible for humans to read? Would we
[58:51] use that language and not the languages
[58:53] that are that are have ergonomics for
[58:57] humans? And I think the answer is yes,
[58:59] we would as soon as we trust because the
[01:00:02] BA systems are going to behave the way
[01:00:04] we want them to behave. Pete, you're
[01:00:05] very welcome. Um, this is just me being
[01:00:09] a geek doing geeky stuff. I'd do this if
[01:00:12] the camera was not rolling.
[01:00:15] Um,
[01:00:17] where are we? Where are we? Okay.
[01:00:22] Uh, okay. So performance trend for large
[01:00:25] data sets GPU put 37.
[01:00:32] Oh, how is it? Uh how is perf
[01:00:38] uh visa
[01:00:42] v CPU? There we go. I'm just since we
[01:00:47] care about performance, I'm going to
[01:00:48] check in on performance
[01:00:51] uh frequently.
[01:00:52] Um, okay. So, Mike, are we writing code
[01:00:55] for humans? Yes, we're still writing
[01:00:57] code for humans because humans,
[01:01:00] if we treat this as a learning
[01:01:02] opportunity,
[01:01:06] then what the code looks like changes
[01:01:09] how easily I can read it. So, you could
[01:01:13] say, oh, WGPU's got this really
[01:01:16] complicated, messy, low-level API.
[01:01:20] Who cares? As long as stuff works. Well,
[01:01:23] I care because I'm trying to learn about
[01:01:28] what's possible on a GPU. And I can't do
[01:01:32] that if I don't understand.
[01:01:35] So for me it is for the moment really
[01:01:40] important
[01:01:41] how the code reads that I have highly
[01:01:45] cohesive loosely coupled elements that
[01:01:49] makes a difference in how I can
[01:01:51] understand things and if I don't
[01:01:54] understand it I can't keep the genie
[01:01:56] from making mistakes which it is prone
[01:01:59] to do. So,
[01:01:04] wow.
[01:01:06] CPU put
[01:01:08] versus GPU put
[01:01:11] were 3x faster on the GPU with a million
[01:01:15] elements
[01:01:17] and the get were 30 times faster. Wow.
[01:01:23] Wow.
[01:01:28] Okay. So, that's interesting. I'm going
[01:01:30] to continue working on this. I hope you
[01:01:32] will take a shot at it, too.
[01:01:36] Um,
[01:01:37] this is complicated enough code that
[01:01:42] the genie can't just copy known
[01:01:45] solutions. If you ask it to write a
[01:01:48] JUnit, it'll just write a Jun because
[01:01:50] it's seen JUnit a million times. This is
[01:01:52] complicated stuff. Topped out at 36
[01:01:55] viewers and that's only paying
[01:01:58] subscribers. Thank you so much. And
[01:01:59] thank you so much for being paying
[01:02:01] subscribers.
[01:02:03] I really appreciate it. Um, this is all
[01:02:06] going to go up on YouTube
[01:02:10] sometime in the near future. Um, I told
[01:02:14] you where the
[01:02:16] [clears throat] on GitHub
[01:02:18] can't be
[01:02:20] GPU sorted map. [snorts]
[01:02:24] Fork it. Get a genie to run on it. Try a
[01:02:29] million different things. Be prepared to
[01:02:31] throw away a bunch of results.
[01:02:34] Learn stuff. Maximize your learning.
[01:02:37] That's if there's one thing uh I would
[01:02:40] say is is do that. Thank you all so
[01:02:43] much. So [snorts] much for the questions
[01:02:45] and comments as we went along. Uh I will
[01:02:48] figure out how to be more engaged with
[01:02:51] whatever the real time user interface is
[01:02:53] once I find it.
[01:02:55] Uh, I hope you all have a fantastic
[01:02:59] um,
[01:03:02] uh, fantastic weekend. I'm going to go
[01:03:05] play some poker. Not right now. I got
[01:03:07] some work to do. Um, I'm going to go
[01:03:10] play some poker and then I'm going to a
[01:03:12] crab feed.
[01:03:14] Uh, so that's my weekend. I hope you
[01:03:17] have a great time.
[01:03:20] Peace.
