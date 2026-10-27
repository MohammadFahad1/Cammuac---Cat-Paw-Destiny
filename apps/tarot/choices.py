import random

CAT_TAROT_CARDS = [
    {
        "id": 1,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "A New Beginning", "zh": "新的開始"},
        "content": {
            "en": "Today is a great time to start fresh. Let go of past worries, embrace new possibilities, and good fortune is coming your way.",
            "zh": "今天是重新出發的好時機。放下過去的擔憂，勇敢迎接新的可能性，幸運正在靠近你。"
        }
    },
    {
        "id": 2,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Follow Your Intuition", "zh": "傾聽直覺"},
        "content": {
            "en": "Cats trust their instincts without hesitation. Take a quiet moment today to listen to your inner voice—it knows the path ahead.",
            "zh": "貓咪總是毫不猶豫地相信直覺。今天給自己片刻安靜，傾聽內心的聲音，它知道前方的路。"
        }
    },
    {
        "id": 3,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "The Art of Rest", "zh": "休息的藝術"},
        "content": {
            "en": "Curling up in the warm sunshine restores the spirit. Give yourself permission to pause and recharge; rest is an essential part of progress.",
            "zh": "在溫暖的陽光下蜷縮小憩，能療癒心靈。允許自己停下腳步充充電，適度的休息也是前進的一部分。"
        }
    },
    {
        "id": 4,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Playful Curiosity", "zh": "玩心與好奇"},
        "content": {
            "en": "Approach the world with open eyes and a playful heart. An unexpected delight is waiting around the next corner.",
            "zh": "帶著好奇的雙眼與玩心探索世界。一個意想不到的小驚喜，正等在下一個轉角處。"
        }
    },
    {
        "id": 5,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Quiet Confidence", "zh": "靜默的自信"},
        "content": {
            "en": "You don't need to roar to demonstrate your strength. Walk with gentle composure and trust in your own remarkable capability.",
            "zh": "不必張揚咆哮，也能展現強大力量。邁出從容輕盈的步伐，深信自己無可替代的能力。"
        }
    },
    {
        "id": 6,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Patient Waiting", "zh": "耐心的守候"},
        "content": {
            "en": "The finest hunter knows when to wait quietly. What you have planted with care is steadily growing; give it time to bloom.",
            "zh": "最頂尖的獵手懂得靜心守候。你用心播下的種子正在悄然萌芽，給它一點時間綻放。"
        }
    },
    {
        "id": 7,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Gentle Boundaries", "zh": "溫柔的界線"},
        "content": {
            "en": "A cat clearly knows when to say no. Protecting your peace of mind is an act of deep self-respect and love.",
            "zh": "貓咪最懂得何時優雅地說不。守護自己內心的平靜，是對自己最深沉的尊重與愛護。"
        }
    },
    {
        "id": 8,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Pure Delight", "zh": "純粹的喜悅"},
        "content": {
            "en": "Notice the simple gifts today: a warm cup, a gentle breeze, a fond memory. Happiness is made of little moments.",
            "zh": "留意今日身邊簡單的贈禮：一杯溫熱的飲品、一陣微風、一段溫暖的回憶。幸福正是由這些微小時刻編織而成。"
        }
    },
    {
        "id": 9,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Leap with Courage", "zh": "勇敢一躍"},
        "content": {
            "en": "The gap may look wide, but your landing will be graceful. Take that bold step forward—you are ready for this leap.",
            "zh": "距離看似遙遠，但你的落地將格外輕盈優雅。勇敢向前邁出那一步，你已經準備好迎接挑戰。"
        }
    },
    {
        "id": 10,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Harmony & Balance", "zh": "和諧與平衡"},
        "content": {
            "en": "Find equilibrium between ambition and relaxation. Like walking a narrow fence, balance comes from focus and staying calm.",
            "zh": "在積極進取與放鬆放手之間找到平衡。如同優雅地走在籬笆上，內心的沉著將帶給你穩定的力量。"
        }
    },
    {
        "id": 11,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Let Go of Control", "zh": "放下執念"},
        "content": {
            "en": "Not every dropped toy is a catastrophe. Release the need to manage every detail and allow life to unfold naturally today.",
            "zh": "並非每一次失手都是遺憾。放下想要掌控所有細節的心態，順應自然，讓生活以最自在的節奏展開。"
        }
    },
    {
        "id": 12,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Warm Companionship", "zh": "溫暖相伴"},
        "content": {
            "en": "Sharing warmth with a kindred soul doubles your joy. Reach out to a friend or simply appreciate the presence of loved ones.",
            "zh": "與知心的夥伴共享溫暖，快樂便會加倍。給好友發個問候，或默默珍惜身邊陪伴你的每一個人。"
        }
    },
    {
        "id": 13,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Focus on the Present", "zh": "專注當下"},
        "content": {
            "en": "The past has slipped away and the future has not arrived. Dedicate your full attention to this very breath and moment.",
            "zh": "過去已悄然溜走，未來尚未來臨。將你的全部心神，傾注在當下的每一次呼吸與體驗之中。"
        }
    },
    {
        "id": 14,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Abundance Within", "zh": "內在豐足"},
        "content": {
            "en": "True wealth is having enough to feel deeply content. Count your blessings today; you possess far more than you realize.",
            "zh": "真正的豐足源自於懂得內心的知足。數一數身邊擁有的美好，你所擁有的遠比想像中更加豐富。"
        }
    },
    {
        "id": 15,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Healing Softness", "zh": "柔軟療癒"},
        "content": {
            "en": "Soft paws tread lightly across sharp stones. Treat yourself with exceptional tenderness today; you have been doing your best.",
            "zh": "柔軟的肉墊能輕盈走過尖銳的碎石。今天對自己多一點溫柔與寬容，你一直都做得很好。"
        }
    },
    {
        "id": 16,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Uncharted Territory", "zh": "探索未知"},
        "content": {
            "en": "Step into an unfamiliar street or try something new today. Stepping outside your routine will bring fresh inspiration.",
            "zh": "走一條未曾走過的小路，或嘗試一件新鮮事物。跳出日常的既定軌道，將為你帶來滿滿的新靈感。"
        }
    },
    {
        "id": 17,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Grace in Transition", "zh": "轉變中的從容"},
        "content": {
            "en": "Seasons shift and winds change, yet cats always land on their feet. Embrace changes in your routine with ease and trust.",
            "zh": "季節流轉、風向變換，但貓咪總能安穩平穩落地。以從容信任的心態，接納生活中的每一處轉變。"
        }
    },
    {
        "id": 18,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Solitary Peace", "zh": "獨處的清幽"},
        "content": {
            "en": "Cherish a quiet hour with just your own thoughts. Solitude is not loneliness; it is a sacred space for your soul to breathe.",
            "zh": "享受一段只屬於自己的安靜時光。獨處並非孤單，而是讓心靈自由呼吸、回歸本真的神聖空間。"
        }
    },
    {
        "id": 19,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Sparks of Inspiration", "zh": "靈感之光"},
        "content": {
            "en": "A sudden flash of clarity will illuminate an old puzzle. Keep a pen nearby—your creative spark is ready to shine brightly.",
            "zh": "一道突如其來的靈感將照亮心中的疑惑。隨時記下閃現的想法，你的創造力正在璀璨發光。"
        }
    },
    {
        "id": 20,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Inner Strength", "zh": "內在堅韌"},
        "content": {
            "en": "Beneath soft fur lies quick agility and stubborn resilience. You are far stronger and more adaptable than any obstacle.",
            "zh": "在柔軟的絨毛之下，蘊藏著敏捷與頑強的韌性。你遠比眼前的任何阻礙都更加強大且富有適應力。"
        }
    },
    {
        "id": 21,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Gratitude & Contentment", "zh": "感恩與知足"},
        "content": {
            "en": "When you appreciate what is already in your bowl, life feels rich and satisfying. Offer heartfelt thanks for today's comfort.",
            "zh": "當你珍惜碗中所擁有的一切，生活便充滿了滋味與滿足。為今日所獲得的平安與舒適致上誠摯的感謝。"
        }
    },
    {
        "id": 22,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Release and Purr", "zh": "釋懷與釋放"},
        "content": {
            "en": "Shake off the dust and tensions of yesterday. A soothing deep sigh or a relaxed stretch will restore your lightness.",
            "zh": "抖落昨日的塵埃與緊繃情緒。一次放鬆的深呼吸與伸展，將使身心重新回復輕盈自在。"
        }
    },
    {
        "id": 23,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Kindness Returned", "zh": "善意的迴響"},
        "content": {
            "en": "A small act of gentle kindness creates ripples of good fortune. Share a sincere smile or encouraging word today.",
            "zh": "微小的善意會在生活中泛起幸運的漣漪。今天向他人送出一個真誠的微笑或一句溫暖的鼓勵吧。"
        }
    },
    {
        "id": 24,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Clear Vision", "zh": "明晰洞察"},
        "content": {
            "en": "Like cats seeing clearly in the dark, your eyes will penetrate the fog. Trust your clarity when making decisions today.",
            "zh": "如同貓咪在夜色中依然雙眸明亮，你也能看清迷霧背後的真相。今天請堅信自己清晰明辨的洞察力。"
        }
    },
    {
        "id": 25,
        "category": {"en": "Today's Guidance", "zh": "今日指引"},
        "title": {"en": "Serendipity", "zh": "美麗的巧合"},
        "content": {
            "en": "Trust the subtle rhythms of serendipity. What seems like an accident is gently guiding you to the right place at the right time.",
            "zh": "相信緣分與巧合的微妙律動。看似偶然的相遇，正在悄然引導你在對的時間抵達對的彼岸。"
        }
    },
    {
        "id": 26,
        "category": {"en": "Love & Relationships", "zh": "愛情與人際關係"},
        "title": {"en": "A Heart Open to Love", "zh": "敞開心扉"},
        "content": {
            "en": "A cat approaches trust one gentle step at a time. Allow yourself to be vulnerable with those who have earned your trust, and let genuine connections grow naturally.",
            "zh": "貓咪總是一步一步地建立信任。試著向值得信賴的人敞開心扉，讓真誠的連結在自然中慢慢成長。"
        }
    },
    {
        "id": 27,
        "category": {"en": "Love & Relationships", "zh": "愛情與人際關係"},
        "title": {"en": "The Language of Love", "zh": "愛的語言"},
        "content": {
            "en": "Not every expression of love needs grand gestures. A thoughtful message, a patient ear, or simply being present can speak louder than a thousand words.",
            "zh": "愛不一定需要轟轟烈烈的表達。一則貼心的訊息、一雙願意傾聽的耳朵，或只是靜靜陪伴，都勝過千言萬語。"
        }
    },
    {
        "id": 28,
        "category": {"en": "Love & Relationships", "zh": "愛情與人際關係"},
        "title": {"en": "The Right Distance", "zh": "恰到好處的距離"},
        "content": {
            "en": "Even the most affectionate cat needs its own space. Healthy relationships allow closeness without control and freedom without fear. Honor the space both you and others need.",
            "zh": "即使最親人的貓咪，也需要屬於自己的空間。健康的關係容得下親密而不控制，也容得下自由而不恐懼。尊重彼此所需要的距離。"
        }
    },
    {
        "id": 29,
        "category": {"en": "Love & Relationships", "zh": "愛情與人際關係"},
        "title": {"en": "Mending the Bond", "zh": "修復彼此的連結"},
        "content": {
            "en": "A moment of misunderstanding does not have to become a lasting distance. Approach difficult conversations with honesty and compassion, and give healing room to begin.",
            "zh": "一時的誤解，不必成為長久的隔閡。以真誠與同理心面對困難的對話，為彼此的修復留出空間。"
        }
    },
    {
        "id": 30,
        "category": {"en": "Love & Relationships", "zh": "愛情與人際關係"},
        "title": {"en": "Love Yourself First", "zh": "先學會愛自己"},
        "content": {
            "en": "A cat never apologizes for taking a comfortable nap. Remember that your needs matter too. Give yourself the care, respect, and tenderness you so freely offer others.",
            "zh": "貓咪從不為自己舒適地小睡片刻而道歉。別忘了，你的需求同樣重要。把你慷慨給予他人的關懷、尊重與溫柔，也留一些給自己。"
        }
    },
    {
        "id": 31,
        "category": {"en": "Career & Purpose", "zh": "事業與人生方向"},
        "title": {"en": "The Perfect Pounce", "zh": "精準的一躍"},
        "content": {
            "en": "A cat studies its target before making a move. Observe your opportunities, prepare carefully, and act when the moment is right. Thoughtful action can turn potential into progress.",
            "zh": "貓咪總會在出擊前仔細觀察目標。留意眼前的機會，做好準備，並在適當的時刻採取行動。深思熟慮的行動，能將潛力化為進步。"
        }
    },
    {
        "id": 32,
        "category": {"en": "Career & Purpose", "zh": "事業與人生方向"},
        "title": {"en": "A Door Opens", "zh": "機會之門"},
        "content": {
            "en": "An unexpected opportunity may invite you to explore unfamiliar territory. Stay prepared, ask thoughtful questions, and remain open to possibilities beyond your usual path.",
            "zh": "一個意想不到的機會，或許正邀請你探索陌生的領域。保持準備、提出有深度的問題，並對既有道路之外的可能性敞開心胸。"
        }
    },
    {
        "id": 33,
        "category": {"en": "Career & Purpose", "zh": "事業與人生方向"},
        "title": {"en": "Master Your Craft", "zh": "精進你的本領"},
        "content": {
            "en": "A cat perfects its movements through countless small adjustments. Your skills grow in the same way. Practice with patience, learn from mistakes, and let consistent effort shape your mastery.",
            "zh": "貓咪透過無數次細微的調整，讓每個動作更加純熟。你的技能也會如此成長。耐心練習、從錯誤中學習，讓持續的努力成就你的專業。"
        }
    },
    {
        "id": 34,
        "category": {"en": "Career & Purpose", "zh": "事業與人生方向"},
        "title": {"en": "Your Own Path", "zh": "走自己的路"},
        "content": {
            "en": "Cats rarely follow a path simply because others do. Release the pressure to imitate someone else's success and discover the rhythm that works for your own ambitions and values.",
            "zh": "貓咪不會只因為別人如此行動，就盲目跟隨。放下模仿他人成功的壓力，找出符合自己目標與價值觀的步調。"
        }
    },
    {
        "id": 35,
        "category": {"en": "Career & Purpose", "zh": "事業與人生方向"},
        "title": {"en": "The Seeds of Success", "zh": "成功的種子"},
        "content": {
            "en": "Not every seed sprouts overnight. Keep nurturing your plans with practical steps and steady commitment. The foundations you build today can support tomorrow's achievements.",
            "zh": "並非每一顆種子都能在一夜之間發芽。持續以實際行動和堅定的投入培育你的計畫。今天打下的基礎，將有助於成就明日的成果。"
        }
    },
    {
        "id": 36,
        "category": {"en": "Abundance & Prosperity", "zh": "豐盛與繁榮"},
        "title": {"en": "The Open Bowl", "zh": "敞開的食碗"},
        "content": {
            "en": "Abundance begins with recognizing what is available to you and using it wisely. Appreciate your resources, remain alert to new opportunities, and take practical steps toward greater stability.",
            "zh": "豐盛始於看見自己所擁有的資源，並懂得善加運用。珍惜手中的一切，留意新的機會，並以實際行動建立更穩固的生活。"
        }
    },
    {
        "id": 37,
        "category": {"en": "Abundance & Prosperity", "zh": "豐盛與繁榮"},
        "title": {"en": "Wise Stewardship", "zh": "智慧理財"},
        "content": {
            "en": "A clever cat knows the value of conserving its energy. Treat your money, time, and attention with similar care. Thoughtful choices today can create greater freedom tomorrow.",
            "zh": "聰明的貓咪懂得珍惜自己的體力。以同樣的態度管理金錢、時間與注意力。今天做出明智的選擇，能為明天創造更多自由。"
        }
    },
    {
        "id": 38,
        "category": {"en": "Abundance & Prosperity", "zh": "豐盛與繁榮"},
        "title": {"en": "Room for More", "zh": "為豐盛留白"},
        "content": {
            "en": "A cluttered corner leaves little room for a new favorite resting spot. Clear away what no longer serves you, whether it is an old habit, an outdated plan, or an unnecessary expense.",
            "zh": "雜亂的角落，難以容納新的舒適之處。清理那些不再適合你的事物，無論是舊習慣、過時的計畫，還是不必要的開銷。"
        }
    },
    {
        "id": 39,
        "category": {"en": "Abundance & Prosperity", "zh": "豐盛與繁榮"},
        "title": {"en": "The Value You Carry", "zh": "你自身的價值"},
        "content": {
            "en": "A cat does not need to resemble another to be remarkable. Recognize the abilities, experiences, and perspective that make you unique, and let them guide the value you bring to the world.",
            "zh": "一隻貓不必與另一隻相似，依然能展現自己的獨特。看見讓你與眾不同的能力、經歷與觀點，並讓它們引領你為世界創造價值。"
        }
    },
    {
        "id": 40,
        "category": {"en": "Abundance & Prosperity", "zh": "豐盛與繁榮"},
        "title": {"en": "A Generous Paw", "zh": "慷慨之爪"},
        "content": {
            "en": "Abundance is not only what you collect but also what you contribute. Share your knowledge, offer a helping hand, and celebrate the success of others without diminishing your own.",
            "zh": "豐盛不只在於你累積了多少，也在於你付出了多少。分享知識、伸出援手，並真心祝福他人的成功，而不因此貶低自己的價值。"
        }
    },
    {
        "id": 41,
        "category": {"en": "Intuition & Wisdom", "zh": "直覺與智慧"},
        "title": {"en": "The Silent Observer", "zh": "沉靜的觀察者"},
        "content": {
            "en": "Before a cat moves, it notices the smallest shift in its surroundings. Slow down enough to observe the details you may have missed. Careful attention can reveal useful insights.",
            "zh": "貓咪在行動之前，總能留意周遭最細微的變化。放慢腳步，觀察那些可能被你忽略的細節。細心留意，往往能帶來有用的啟發。"
        }
    },
    {
        "id": 42,
        "category": {"en": "Intuition & Wisdom", "zh": "直覺與智慧"},
        "title": {"en": "The Inner Compass", "zh": "內心的羅盤"},
        "content": {
            "en": "Your instincts can offer valuable clues, but wisdom also asks you to examine the facts. Listen inwardly, look outwardly, and make your decision with both intuition and reason.",
            "zh": "你的直覺能提供珍貴的線索，但智慧也提醒你檢視客觀事實。傾聽內心、觀察外在，讓直覺與理性共同引領你的決定。"
        }
    },
    {
        "id": 43,
        "category": {"en": "Intuition & Wisdom", "zh": "直覺與智慧"},
        "title": {"en": "Beyond First Impressions", "zh": "超越第一印象"},
        "content": {
            "en": "A shadow on the wall may look like something entirely different in the light. Give people and situations time to reveal their true shape before reaching a conclusion.",
            "zh": "牆上的影子，在光線改變後可能呈現截然不同的模樣。在下定論之前，給人與事一些時間，讓它們展現真實的樣貌。"
        }
    },
    {
        "id": 44,
        "category": {"en": "Intuition & Wisdom", "zh": "直覺與智慧"},
        "title": {"en": "The Wisdom of Silence", "zh": "沉默的智慧"},
        "content": {
            "en": "A cat can sit quietly without needing to fill every moment with noise. Today, allow silence to settle before responding. A thoughtful pause may reveal the words that truly matter.",
            "zh": "貓咪可以安靜地坐著，不必用聲音填滿每一刻。今天，在回應之前，試著讓沉默停留片刻。深思熟慮的停頓，或許能讓真正重要的話語浮現。"
        }
    },
    {
        "id": 45,
        "category": {"en": "Intuition & Wisdom", "zh": "直覺與智慧"},
        "title": {"en": "A Lesson in Patterns", "zh": "從規律中學習"},
        "content": {
            "en": "Cats learn from repeated experiences. Notice the patterns in your own days: what restores your energy, what drains it, and what keeps returning. Awareness gives you the chance to choose differently.",
            "zh": "貓咪會從反覆的經驗中學習。留意日常生活中的規律：什麼讓你恢復活力，什麼消耗你的能量，又有哪些事情一再發生。覺察，讓你有機會做出不同的選擇。"
        }
    },
    {
        "id": 46,
        "category": {"en": "Transformation & Change", "zh": "蛻變與改變"},
        "title": {"en": "A New Coat", "zh": "煥然一新"},
        "content": {
            "en": "As seasons change, a cat's coat changes too. You are allowed to renew your habits, beliefs, and ambitions as you grow. Let go of what no longer fits the person you are becoming.",
            "zh": "隨著季節更迭，貓咪的毛色與狀態也會改變。隨著成長，你也可以更新自己的習慣、信念與目標。放下那些已不再適合現在的你的事物。"
        }
    },
    {
        "id": 47,
        "category": {"en": "Transformation & Change", "zh": "蛻變與改變"},
        "title": {"en": "The Turning Point", "zh": "轉折的時刻"},
        "content": {
            "en": "Sometimes the smallest choice redirects an entire journey. Pay attention to the decision in front of you today. You may not control every outcome, but you can choose your next direction.",
            "zh": "有時，一個微小的選擇就能改變整段旅程。留意今天擺在你面前的決定。你未必能掌控所有結果，但你可以選擇下一個方向。"
        }
    },
    {
        "id": 48,
        "category": {"en": "Transformation & Change", "zh": "蛻變與改變"},
        "title": {"en": "Leaving the Old Nest", "zh": "離開舊有的巢"},
        "content": {
            "en": "Familiar places feel safe, but growth sometimes asks you to explore beyond them. Take one manageable step outside your comfort zone and discover what your world can become.",
            "zh": "熟悉的地方總讓人安心，但成長有時需要你走出去探索。試著踏出舒適圈一小步，看看你的世界還能擁有什麼新的可能。"
        }
    },
    {
        "id": 49,
        "category": {"en": "Transformation & Change", "zh": "蛻變與改變"},
        "title": {"en": "The Power of Release", "zh": "放下的力量"},
        "content": {
            "en": "A cat does not carry yesterday's nap into today's adventure. You can honor your past without remaining trapped in it. Release what you cannot change and use your energy where it can make a difference.",
            "zh": "貓咪不會帶著昨天的小憩，困住今天的冒險。你可以珍惜過去，卻不必被過去束縛。放下無法改變的事，把精力用在真正能帶來改變的地方。"
        }
    },
    {
        "id": 50,
        "category": {"en": "Transformation & Change", "zh": "蛻變與改變"},
        "title": {"en": "The First Light", "zh": "初現的曙光"},
        "content": {
            "en": "The darkest hour is not the whole story of the night. Even when progress feels invisible, small acts of care and courage still matter. Keep moving gently toward the light you can see.",
            "zh": "最深沉的黑夜，並不是整個夜晚的故事。即使進步尚未顯現，微小的關懷與勇氣依然有意義。繼續溫柔而堅定地走向你所看見的光。"
        }
    },
    {
        "id": 51,
        "category": {"en": "Courage & Resilience", "zh": "勇氣與韌性"},
        "title": {"en": "Nine Lives of Courage", "zh": "九命的勇氣"},
        "content": {
            "en": "A cat may retreat, reassess, and try another way. Courage is not the absence of fear; it is the willingness to adapt and continue after a difficult moment.",
            "zh": "貓咪可能會退後、重新觀察，再嘗試另一條路。勇氣並非毫無恐懼，而是在困難之後，依然願意調整自己並繼續前進。"
        }
    },
    {
        "id": 52,
        "category": {"en": "Courage & Resilience", "zh": "勇氣與韌性"},
        "title": {"en": "One Paw at a Time", "zh": "一步一爪印"},
        "content": {
            "en": "A long journey becomes manageable when you focus on the ground beneath your paws. Break today's challenge into smaller actions and complete the next one before worrying about the rest.",
            "zh": "當你專注於腳下的每一步，漫長的旅程也會變得容易應對。把今天的挑戰拆解成更小的行動，先完成眼前的一步，再考慮接下來的事。"
        }
    },
    {
        "id": 53,
        "category": {"en": "Courage & Resilience", "zh": "勇氣與韌性"},
        "title": {"en": "The Art of Trying Again", "zh": "再次嘗試的藝術"},
        "content": {
            "en": "Missing a jump does not mean a cat has forgotten how to leap. Let disappointment teach you what to adjust, then try again when you are ready. A setback can be information, not a verdict.",
            "zh": "一次跳躍失誤，不代表貓咪忘記了如何跳躍。讓失望告訴你需要調整什麼，準備好後再試一次。挫折可以是一種提醒，而不是對你的定論。"
        }
    },
    {
        "id": 54,
        "category": {"en": "Courage & Resilience", "zh": "勇氣與韌性"},
        "title": {"en": "Softness Is Strength", "zh": "溫柔也是力量"},
        "content": {
            "en": "A cat can be both delicate and remarkably resilient. You do not need to become hard to survive difficult seasons. Keep your compassion while learning how to protect your peace.",
            "zh": "貓咪既可以柔軟，也能展現驚人的韌性。你不必為了度過艱難的時期而讓自己變得冷硬。在學會守護內心平靜的同時，也保留你的善良。"
        }
    },
    {
        "id": 55,
        "category": {"en": "Courage & Resilience", "zh": "勇氣與韌性"},
        "title": {"en": "The Brave Little Step", "zh": "勇敢的一小步"},
        "content": {
            "en": "A new room can feel enormous to a small cat. If a challenge seems overwhelming, make the first step tiny. You can build confidence through experience rather than waiting for fear to disappear.",
            "zh": "對一隻小貓而言，一個陌生的房間也可能顯得無比巨大。如果挑戰讓你不知所措，就把第一步縮小。透過親身經歷累積信心，而不是等待恐懼完全消失。"
        }
    },
    {
        "id": 56,
        "category": {"en": "Creativity & Inspiration", "zh": "創意與靈感"},
        "title": {"en": "The Curious Paw", "zh": "好奇之爪"},
        "content": {
            "en": "A simple moving shadow can become a cat's entire adventure. Look at familiar things with fresh eyes today. A small detail may spark a new idea or reveal a different solution.",
            "zh": "一道簡單移動的影子，就能成為貓咪的一場冒險。今天試著用全新的眼光看待熟悉的事物。一個微小的細節，或許就能激發新想法或帶來不同的解決方法。"
        }
    },
    {
        "id": 57,
        "category": {"en": "Creativity & Inspiration", "zh": "創意與靈感"},
        "title": {"en": "Play Before Perfection", "zh": "先玩出創意，再追求完美"},
        "content": {
            "en": "A cat explores before it understands every corner. Give yourself permission to experiment without demanding immediate perfection. Discovery often arrives through playful, imperfect beginnings.",
            "zh": "貓咪總是在完全了解每個角落之前，就開始探索。允許自己自由嘗試，不必一開始就追求完美。許多發現，正是從充滿玩心而不完美的起點誕生。"
        }
    },
    {
        "id": 58,
        "category": {"en": "Creativity & Inspiration", "zh": "創意與靈感"},
        "title": {"en": "A Different Angle", "zh": "換個角度"},
        "content": {
            "en": "Cats see the world from windowsills, rooftops, and hidden corners. If you feel stuck, change your viewpoint. A fresh perspective can transform a familiar obstacle into a solvable puzzle.",
            "zh": "貓咪從窗台、屋頂與隱密的角落觀察世界。如果你感到困住了，不妨換個角度。全新的觀點，能讓熟悉的障礙變成可以解開的謎題。"
        }
    },
    {
        "id": 59,
        "category": {"en": "Creativity & Inspiration", "zh": "創意與靈感"},
        "title": {"en": "The Unwritten Page", "zh": "尚未寫下的篇章"},
        "content": {
            "en": "An empty page is full of possibilities, not proof that you have nothing to offer. Begin with one sentence, one sketch, or one small experiment. Let the work reveal what comes next.",
            "zh": "一張空白的紙充滿可能，並不代表你無話可說。從一句話、一幅草圖或一次小小的實驗開始，讓創作的過程帶領你發現下一步。"
        }
    },
    {
        "id": 60,
        "category": {"en": "Creativity & Inspiration", "zh": "創意與靈感"},
        "title": {"en": "Follow the Spark", "zh": "追隨靈感的火花"},
        "content": {
            "en": "A flicker of curiosity can lead to an unexpected discovery. Write down the idea that excites you, explore it for a little while, and see what it teaches you. Not every spark must become a fire to be worthwhile.",
            "zh": "一絲好奇，可能引領你走向意想不到的發現。記下讓你心動的想法，花一點時間探索，看看它能帶給你什麼啟發。不是每一點火花都必須燃成大火，才具有價值。"
        }
    },
    {
        "id": 61,
        "category": {"en": "Rest & Renewal", "zh": "休息與重生"},
        "title": {"en": "The Sunlit Pause", "zh": "陽光下的停歇"},
        "content": {
            "en": "A cat instinctively seeks a warm patch of sunlight. Create a small pocket of comfort in your day, even if only for a few minutes. You can return to your responsibilities with a little more room to breathe.",
            "zh": "貓咪總會本能地尋找一片溫暖的陽光。即使只有幾分鐘，也為今天的自己留下一小段舒適的時光。當你再次面對責任時，心中或許就能多一點從容。"
        }
    },
    {
        "id": 62,
        "category": {"en": "Rest & Renewal", "zh": "休息與重生"},
        "title": {"en": "The Gentle Reset", "zh": "溫柔地重新開始"},
        "content": {
            "en": "When a cat wakes from a nap, it stretches before moving forward. Give yourself a similar transition. Take a breath, loosen your shoulders, and begin the next part of your day without carrying every earlier tension with you.",
            "zh": "貓咪從小睡中醒來後，總會先伸展身體再繼續活動。也給自己一段這樣的過渡時間。深呼吸、放鬆肩膀，不必把先前的所有緊繃都帶進接下來的時光。"
        }
    },
    {
        "id": 63,
        "category": {"en": "Rest & Renewal", "zh": "休息與重生"},
        "title": {"en": "Permission to Slow Down", "zh": "允許自己慢下來"},
        "content": {
            "en": "Not every day needs to be a race. Move at a pace that respects your energy and circumstances. Slowing down can be a wise adjustment, not a failure to keep up.",
            "zh": "並非每一天都必須像一場競賽。依照自己的精力與處境調整步調。放慢腳步可以是一種明智的調整，而不是跟不上別人的失敗。"
        }
    },
    {
        "id": 64,
        "category": {"en": "Rest & Renewal", "zh": "休息與重生"},
        "title": {"en": "The Quiet Corner", "zh": "安靜的角落"},
        "content": {
            "en": "Every cat appreciates a safe place to retreat. Find a small space where you can put down the day's demands and simply exist. You do not need to be productive in every moment to deserve peace.",
            "zh": "每隻貓咪都需要一個可以安心退回的角落。找一處小小的空間，暫時放下今天的要求，只是自在地存在。你不必時時刻刻有所產出，才值得擁有平靜。"
        }
    },
    {
        "id": 65,
        "category": {"en": "Rest & Renewal", "zh": "休息與重生"},
        "title": {"en": "Restore Your Whiskers", "zh": "重新找回活力"},
        "content": {
            "en": "Even the most energetic cat needs recovery between adventures. Notice what your body and mind are asking for, and respond with care. Sustainable progress includes knowing when to recharge.",
            "zh": "即使精力最旺盛的貓咪，也需要在冒險之間恢復體力。留意身心正在向你發出的訊號，並好好照顧自己。懂得適時充電，也是持續進步的一部分。"
        }
    },
    {
        "id": 66,
        "category": {"en": "Balance & Harmony", "zh": "平衡與和諧"},
        "title": {"en": "The Balanced Cat", "zh": "平衡的貓咪"},
        "content": {
            "en": "A cat alternates between lively play and deep rest. Let your day contain both effort and recovery. You can pursue meaningful goals without treating every quiet moment as wasted time.",
            "zh": "貓咪會在活潑玩耍與深沉休息之間自在切換。讓今天同時容納努力與恢復。你可以追求有意義的目標，而不必把每個安靜的時刻都視為浪費。"
        }
    },
    {
        "id": 67,
        "category": {"en": "Balance & Harmony", "zh": "平衡與和諧"},
        "title": {"en": "Two Paws on the Ground", "zh": "腳踏實地"},
        "content": {
            "en": "When the world feels uncertain, return to what you can actually do today. Separate real responsibilities from imagined worries and give your attention to the next practical step.",
            "zh": "當世界讓你感到不確定時，回到今天真正能做到的事情上。分清實際的責任與想像中的憂慮，把注意力放在下一個可行的步驟。"
        }
    },
    {
        "id": 68,
        "category": {"en": "Balance & Harmony", "zh": "平衡與和諧"},
        "title": {"en": "The Middle Path", "zh": "中庸之道"},
        "content": {
            "en": "A cat knows when to leap and when to remain still. You do not have to choose between constant action and complete withdrawal. Seek a rhythm that leaves room for ambition, connection, and rest.",
            "zh": "貓咪知道何時躍起，也知道何時靜止。你不必在不停行動與完全退縮之間二選一。尋找一種能同時容納抱負、連結與休息的生活節奏。"
        }
    },
    {
        "id": 69,
        "category": {"en": "Balance & Harmony", "zh": "平衡與和諧"},
        "title": {"en": "The Flexible Branch", "zh": "柔韌的枝條"},
        "content": {
            "en": "A flexible branch bends with the wind without losing its roots. Stay open to changing your methods while remaining connected to what matters most. Adaptability can protect your purpose when circumstances shift.",
            "zh": "柔韌的枝條隨風彎曲，卻不會失去根基。保持調整方法的彈性，同時不忘最重要的價值。當環境改變時，適應力能幫助你守住初心。"
        }
    },
    {
        "id": 70,
        "category": {"en": "Balance & Harmony", "zh": "平衡與和諧"},
        "title": {"en": "Enough for Today", "zh": "今天已經足夠"},
        "content": {
            "en": "A day does not need to contain every achievement you hoped for. Acknowledge what you completed, learn from what remains, and let yourself close the day with a sense of perspective rather than endless self-criticism.",
            "zh": "一天之中，不必完成所有期待中的成就。肯定已經完成的事，從尚未完成的部分學習，並帶著適度的自我理解結束今天，而不是陷入無止境的自我批評。"
        }
    },
    {
        "id": 71,
        "category": {"en": "Gratitude & Joy", "zh": "感恩與喜悅"},
        "title": {"en": "The Gift of Ordinary Things", "zh": "平凡事物的禮物"},
        "content": {
            "en": "A cardboard box can become a palace in a cat's imagination. Let ordinary things surprise you again. A familiar meal, a friendly greeting, or a quiet evening can hold more goodness than you expect.",
            "zh": "在貓咪的想像中，一個紙箱也能成為宮殿。讓平凡的事物再次帶給你驚喜。一頓熟悉的飯、一聲友善的問候，或一個安靜的夜晚，都可能藏著超乎預期的美好。"
        }
    },
    {
        "id": 72,
        "category": {"en": "Gratitude & Joy", "zh": "感恩與喜悅"},
        "title": {"en": "A Moment Worth Keeping", "zh": "值得珍藏的瞬間"},
        "content": {
            "en": "Some moments are small enough to pass unnoticed and precious enough to remember for years. Pause when something makes you smile. Let yourself fully experience the good that is already here.",
            "zh": "有些瞬間微小得容易被忽略，卻珍貴得足以讓人記住多年。當某件事讓你微笑時，停下來好好感受，珍惜此刻已經存在的美好。"
        }
    },
    {
        "id": 73,
        "category": {"en": "Gratitude & Joy", "zh": "感恩與喜悅"},
        "title": {"en": "The Warm Welcome", "zh": "溫暖的迎接"},
        "content": {
            "en": "A familiar presence can make even an ordinary return feel special. Express appreciation to someone who brings comfort to your life, and do not assume they already know how much they matter.",
            "zh": "熟悉的陪伴，能讓一次平凡的歸來也變得特別。向那個為你帶來安心的人表達感謝，別以為對方一定知道自己有多重要。"
        }
    },
    {
        "id": 74,
        "category": {"en": "Gratitude & Joy", "zh": "感恩與喜悅"},
        "title": {"en": "The Bright Side of Rain", "zh": "雨天的另一面"},
        "content": {
            "en": "Rain may interrupt a cat's outdoor adventure, but it can also make a cozy afternoon. When plans change, look for what remains possible. Disappointment and unexpected comfort can exist in the same day.",
            "zh": "雨水或許打亂了貓咪外出的冒險，卻也能帶來舒適的午後。當計畫改變時，試著看看還有哪些可能。失望與意外的安慰，可以同時存在於同一天。"
        }
    },
    {
        "id": 75,
        "category": {"en": "Gratitude & Joy", "zh": "感恩與喜悅"},
        "title": {"en": "Celebrate the Small Win", "zh": "慶祝微小的勝利"},
        "content": {
            "en": "Every successful little leap deserves a moment of recognition. Notice the task you finally started, the boundary you maintained, or the kindness you offered. Small wins help make progress visible.",
            "zh": "每一次成功的小小躍進，都值得被看見。留意你終於開始的任務、堅守的界線，或付出的善意。微小的勝利，能讓進步變得清晰可見。"
        }
    },
    {
        "id": 76,
        "category": {"en": "Spiritual Reflection", "zh": "心靈沉思"},
        "title": {"en": "The Space Between Thoughts", "zh": "念頭之間的空間"},
        "content": {
            "en": "You are more than the thoughts passing through your mind. Observe them without needing to chase every one or push every one away. A little mental space can help you respond with greater clarity.",
            "zh": "你不只是腦海中來來去去的念頭。試著觀察它們，不必追逐每一個念頭，也不必刻意排斥它們。為思緒留出一點空間，能幫助你更清晰地回應生活。"
        }
    },
    {
        "id": 77,
        "category": {"en": "Spiritual Reflection", "zh": "心靈沉思"},
        "title": {"en": "Trust Without Certainty", "zh": "在不確定中前行"},
        "content": {
            "en": "A cat does not need to see the entire path to take its next step. You may not have every answer today. Work with what you know, stay open to learning, and allow the rest to become clearer in time.",
            "zh": "貓咪不必看清整條道路，才能踏出下一步。今天的你或許還沒有所有答案。先運用已知的資訊，保持學習的開放態度，讓其餘的方向隨時間逐漸清晰。"
        }
    },
    {
        "id": 78,
        "category": {"en": "Spiritual Reflection", "zh": "心靈沉思"},
        "title": {"en": "The Quiet Knowing", "zh": "靜心中的明白"},
        "content": {
            "en": "Sometimes clarity arrives after you stop forcing an answer. Step back from the noise, give yourself time to reflect, and distinguish what you genuinely believe from what you feel pressured to believe.",
            "zh": "有時，當你不再強迫自己尋找答案，清晰的思路反而會自然浮現。暫時遠離喧囂，給自己一些反思的時間，分辨真正相信的事與因壓力而被迫接受的想法。"
        }
    },
    {
        "id": 79,
        "category": {"en": "Spiritual Reflection", "zh": "心靈沉思"},
        "title": {"en": "A Thread of Meaning", "zh": "意義的絲線"},
        "content": {
            "en": "Not every experience reveals its meaning immediately. Allow yourself to learn as life unfolds, without forcing every event into a grand explanation. Sometimes meaning grows through what you choose to do next.",
            "zh": "並非每一段經歷都會立即顯現它的意義。讓自己隨著生活的展開慢慢學習，不必強迫每件事都擁有宏大的解釋。有時，意義是在你接下來的選擇中逐漸形成的。"
        }
    },
    {
        "id": 80,
        "category": {"en": "Spiritual Reflection", "zh": "心靈沉思"},
        "title": {"en": "The Sacred Ordinary", "zh": "平凡中的珍貴"},
        "content": {
            "en": "A quiet meal, a caring gesture, or a moment of honest reflection can make a day feel meaningful. You do not need a dramatic sign to appreciate the life unfolding around you.",
            "zh": "一頓安靜的飯、一個關懷的舉動，或一段真誠的自我反思，都能讓一天變得有意義。珍惜正在展開的生活，不需要等待戲劇性的徵兆。"
        }
    },
]


def get_random_tarot_card():
    """
    Randomly selects one Cat Tarot card from the pre-defined pool.
    """
    return random.choice(CAT_TAROT_CARDS)


def get_all_tarot_choices():
    """
    Returns the full list of available Cat Tarot choices.
    """
    return CAT_TAROT_CARDS

