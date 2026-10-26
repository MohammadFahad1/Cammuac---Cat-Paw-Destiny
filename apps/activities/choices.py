import random

GOOD_FOR_CHOICES = [
    # Personal Growth
    {"en": "Effort", "zh": "努力"},
    {"en": "Learning", "zh": "學習"},
    {"en": "Discipline", "zh": "自律"},
    {"en": "Courage", "zh": "勇氣"},
    {"en": "Confidence", "zh": "自信"},
    {"en": "Consistency", "zh": "持之以恆"},
    {"en": "Self-Improvement", "zh": "自我提升"},
    {"en": "Growth", "zh": "成長"},
    {"en": "Resilience", "zh": "韌性"},
    {"en": "Curiosity", "zh": "好奇心"},
    {"en": "Wisdom", "zh": "智慧"},
    {"en": "Honesty", "zh": "誠實"},
    {"en": "Responsibility", "zh": "責任感"},
    {"en": "Perseverance", "zh": "堅持不懈"},
    {"en": "Positive Thinking", "zh": "正向思考"},
    {"en": "Acceptance", "zh": "接納"},
    {"en": "Letting Go", "zh": "放下"},
    {"en": "Open-Mindedness", "zh": "開放心態"},

    # Happiness & Emotions
    {"en": "Smiles", "zh": "微笑"},
    {"en": "Laughter", "zh": "歡笑"},
    {"en": "Happiness", "zh": "快樂"},
    {"en": "Joy", "zh": "喜悅"},
    {"en": "Gratitude", "zh": "感恩"},
    {"en": "Optimism", "zh": "樂觀"},
    {"en": "Hope", "zh": "希望"},
    {"en": "Contentment", "zh": "知足"},
    {"en": "Peace of Mind", "zh": "心靈平靜"},
    {"en": "Emotional Balance", "zh": "情緒平衡"},
    {"en": "Self-Acceptance", "zh": "自我接納"},
    {"en": "Forgiveness", "zh": "寬恕"},
    {"en": "Calmness", "zh": "平靜"},
    {"en": "Mindfulness", "zh": "正念"},
    {"en": "Enjoying the Moment", "zh": "享受當下"},

    # Health & Wellness
    {"en": "Meditation", "zh": "冥想"},
    {"en": "Exercise", "zh": "運動"},
    {"en": "Walking", "zh": "散步"},
    {"en": "Stretching", "zh": "伸展運動"},
    {"en": "Healthy Eating", "zh": "健康飲食"},
    {"en": "Drinking Water", "zh": "補充水分"},
    {"en": "Quality Sleep", "zh": "優質睡眠"},
    {"en": "Rest", "zh": "適度休息"},
    {"en": "Deep Breathing", "zh": "深呼吸"},
    {"en": "Fresh Air", "zh": "呼吸新鮮空氣"},
    {"en": "Spending Time Outdoors", "zh": "親近大自然"},
    {"en": "Self-Care", "zh": "關愛自我"},
    {"en": "Healthy Habits", "zh": "健康習慣"},
    {"en": "Relaxation", "zh": "放鬆"},
    {"en": "Digital Detox", "zh": "數位排毒"},
    {"en": "Taking Breaks", "zh": "適時休息"},

    # Kindness & Relationships
    {"en": "Kindness", "zh": "行善"},
    {"en": "Sharing", "zh": "分享"},
    {"en": "Listening", "zh": "傾聽"},
    {"en": "Patience", "zh": "耐心"},
    {"en": "Empathy", "zh": "同理心"},
    {"en": "Compassion", "zh": "慈悲"},
    {"en": "Generosity", "zh": "慷慨"},
    {"en": "Respect", "zh": "尊重"},
    {"en": "Understanding", "zh": "理解"},
    {"en": "Cooperation", "zh": "合作"},
    {"en": "Teamwork", "zh": "團隊合作"},
    {"en": "Communication", "zh": "溝通"},
    {"en": "Connection", "zh": "建立連結"},
    {"en": "Quality Time", "zh": "珍惜相處時光"},
    {"en": "Helping Others", "zh": "幫助他人"},
    {"en": "Encouragement", "zh": "鼓勵"},
    {"en": "Appreciation", "zh": "感謝與欣賞"},
    {"en": "Trust", "zh": "信任"},
    {"en": "Building Friendships", "zh": "建立友誼"},
    {"en": "Acts of Service", "zh": "付諸行動的關懷"},

    # Productivity & Focus
    {"en": "Deep Focus", "zh": "專注"},
    {"en": "Organization", "zh": "斷捨離"},
    {"en": "Planning", "zh": "規劃"},
    {"en": "Goal Setting", "zh": "設定目標"},
    {"en": "Time Management", "zh": "時間管理"},
    {"en": "Prioritization", "zh": "排定優先順序"},
    {"en": "Taking Action", "zh": "付諸行動"},
    {"en": "Problem Solving", "zh": "解決問題"},
    {"en": "Decision Making", "zh": "做出決策"},
    {"en": "Decluttering", "zh": "整理與斷捨離"},
    {"en": "Completing Tasks", "zh": "完成任務"},
    {"en": "Working Smart", "zh": "聰明工作"},
    {"en": "Persistence", "zh": "堅忍不拔"},
    {"en": "Preparation", "zh": "事前準備"},
    {"en": "Reflection", "zh": "反思"},
    {"en": "Taking Initiative", "zh": "主動積極"},

    # Learning & Creativity
    {"en": "Reading", "zh": "閱讀"},
    {"en": "Creativity", "zh": "創作"},
    {"en": "Writing", "zh": "寫作"},
    {"en": "Journaling", "zh": "寫日記"},
    {"en": "Drawing", "zh": "繪畫"},
    {"en": "Music", "zh": "音樂"},
    {"en": "Photography", "zh": "攝影"},
    {"en": "Learning Languages", "zh": "學習語言"},
    {"en": "Critical Thinking", "zh": "批判性思考"},
    {"en": "Experimentation", "zh": "勇於嘗試"},
    {"en": "Innovation", "zh": "創新"},
    {"en": "Exploration", "zh": "探索新事物"},
    {"en": "Skill Building", "zh": "培養技能"},
    {"en": "Knowledge Sharing", "zh": "分享知識"},
    {"en": "Asking Questions", "zh": "提出問題"},
    {"en": "Trying Something New", "zh": "嘗試新事物"},

    # Nature & Everyday Life
    {"en": "Sunshine", "zh": "陽光"},
    {"en": "Nature", "zh": "大自然"},
    {"en": "Gardening", "zh": "園藝"},
    {"en": "Exploring New Places", "zh": "探索新地方"},
    {"en": "Travel", "zh": "旅行"},
    {"en": "Simplicity", "zh": "簡約生活"},
    {"en": "Living Slowly", "zh": "慢活"},
    {"en": "Being Present", "zh": "活在當下"},
    {"en": "Enjoying Small Things", "zh": "享受生活中的小美好"},
    {"en": "New Experiences", "zh": "全新體驗"},
    {"en": "Spontaneity", "zh": "隨性而行"},
    {"en": "Adventure", "zh": "冒險"},
    {"en": "Wonder", "zh": "驚奇"},
    {"en": "Appreciating Beauty", "zh": "欣賞美好"},
    {"en": "Daily Rituals", "zh": "日常儀式感"},

    # Purpose & Inner Values
    {"en": "Purpose", "zh": "人生目標"},
    {"en": "Meaningful Work", "zh": "有意義的工作"},
    {"en": "Authenticity", "zh": "真誠做自己"},
    {"en": "Integrity", "zh": "正直"},
    {"en": "Balance", "zh": "平衡"},
    {"en": "Freedom", "zh": "自由"},
    {"en": "Independence", "zh": "獨立"},
    {"en": "Graciousness", "zh": "優雅與寬厚"},
    {"en": "Humility", "zh": "謙遜"},
    {"en": "Generational Impact", "zh": "為後代創造影響"},
    {"en": "Making a Difference", "zh": "創造正面影響"},
    {"en": "Giving Back", "zh": "回饋社會"},
    {"en": "Living Intentionally", "zh": "有意識地生活"},
    {"en": "Keeping Promises", "zh": "信守承諾"},
    {"en": "Being Yourself", "zh": "做真實的自己"},
]

AVOID_CHOICES = [
    # Emotional Well-being
    {"en": "Anxiety", "zh": "焦慮"},
    {"en": "Overthinking", "zh": "胡思亂想"},
    {"en": "Negative Thinking", "zh": "負面思考"},
    {"en": "Self-doubt", "zh": "自我懷疑"},
    {"en": "Fear of Failure", "zh": "害怕失敗"},
    {"en": "Fear of Rejection", "zh": "害怕被拒絕"},
    {"en": "Dwelling on the Past", "zh": "沉溺於過去"},
    {"en": "Worrying About the Future", "zh": "過度擔憂未來"},
    {"en": "Perfectionism", "zh": "完美主義"},
    {"en": "Unrealistic Expectations", "zh": "不切實際的期望"},
    {"en": "Seeking Constant Validation", "zh": "過度尋求他人認同"},
    {"en": "Taking Things Personally", "zh": "過度往心裡去"},
    {"en": "Holding Grudges", "zh": "心懷怨恨"},
    {"en": "Suppressing Emotions", "zh": "壓抑情緒"},
    {"en": "Emotional Reactivity", "zh": "情緒化反應"},
    {"en": "Catastrophizing", "zh": "災難化思考"},
    {"en": "Guilt Tripping Yourself", "zh": "過度自責"},
    {"en": "Harsh Self-Criticism", "zh": "嚴厲批評自己"},
    {"en": "Jealousy", "zh": "嫉妒"},
    {"en": "Resentment", "zh": "怨懟"},

    # Unhealthy Habits
    {"en": "Staying up late", "zh": "熬夜"},
    {"en": "Excessive Screen Time", "zh": "沉迷手機"},
    {"en": "Mindless Scrolling", "zh": "無意識地滑手機"},
    {"en": "Skipping Meals", "zh": "不按時吃飯"},
    {"en": "Overeating", "zh": "暴飲暴食"},
    {"en": "Emotional Eating", "zh": "情緒性進食"},
    {"en": "Eating Too Much Junk Food", "zh": "過量食用垃圾食物"},
    {"en": "Excessive Caffeine", "zh": "過量攝取咖啡因"},
    {"en": "Neglecting Exercise", "zh": "忽略運動"},
    {"en": "Ignoring Rest", "zh": "忽視休息"},
    {"en": "Ignoring Personal Hygiene", "zh": "忽視個人衛生"},
    {"en": "Sedentary Lifestyle", "zh": "久坐不動的生活方式"},
    {"en": "Neglecting Hydration", "zh": "忽略補充水分"},
    {"en": "Excessive Gaming", "zh": "過度沉迷遊戲"},
    {"en": "Unhealthy Escapism", "zh": "以不健康的方式逃避現實"},
    {"en": "Habitual Multitasking", "zh": "習慣同時處理多項任務"},
    {"en": "Ignoring Warning Signs", "zh": "忽視警訊"},
    {"en": "Overworking", "zh": "過度工作"},
    {"en": "Neglecting Self-Care", "zh": "忽視自我照顧"},

    # Productivity & Time Management
    {"en": "Procrastination", "zh": "拖延"},
    {"en": "Disorganization", "zh": "缺乏條理"},
    {"en": "Poor Time Management", "zh": "時間管理不當"},
    {"en": "Distractions", "zh": "分心"},
    {"en": "Lack of Focus", "zh": "缺乏專注"},
    {"en": "Multitasking Too Much", "zh": "過度分心處理多項任務"},
    {"en": "Avoiding Difficult Tasks", "zh": "逃避困難的任務"},
    {"en": "Analysis Paralysis", "zh": "分析過度而無法行動"},
    {"en": "Overcommitting", "zh": "承諾過多"},
    {"en": "Poor Planning", "zh": "缺乏規劃"},
    {"en": "Last-Minute Rushing", "zh": "臨時抱佛腳"},
    {"en": "Unnecessary Busyness", "zh": "無意義的忙碌"},
    {"en": "Perfectionism at Work", "zh": "工作上的完美主義"},
    {"en": "Neglecting Priorities", "zh": "忽略優先事項"},
    {"en": "Giving Up Too Soon", "zh": "過早放棄"},
    {"en": "Making Excuses", "zh": "找藉口"},
    {"en": "Avoiding Responsibility", "zh": "逃避責任"},
    {"en": "Waiting for Motivation", "zh": "一味等待動力"},
    {"en": "Fear of Starting", "zh": "害怕開始"},
    {"en": "Unfinished Tasks", "zh": "任務半途而廢"},

    # Social Comparison & Relationships
    {"en": "Comparison", "zh": "比較"},
    {"en": "Conflict", "zh": "爭吵"},
    {"en": "Complaining", "zh": "抱怨"},
    {"en": "Impatience", "zh": "急躁"},
    {"en": "Isolation", "zh": "過度封閉"},
    {"en": "People-Pleasing", "zh": "一味討好他人"},
    {"en": "Seeking Approval", "zh": "尋求他人認可"},
    {"en": "Gossiping", "zh": "說閒話"},
    {"en": "Judging Others", "zh": "評判他人"},
    {"en": "Blaming Others", "zh": "責怪他人"},
    {"en": "Interrupting Others", "zh": "打斷他人說話"},
    {"en": "Not Listening", "zh": "不願傾聽"},
    {"en": "Passive Aggression", "zh": "被動攻擊"},
    {"en": "Unnecessary Arguments", "zh": "無謂的爭論"},
    {"en": "Holding Grudges Against Others", "zh": "對他人懷恨在心"},
    {"en": "Unhealthy Boundaries", "zh": "不健康的人際界線"},
    {"en": "Neglecting Loved Ones", "zh": "忽略所愛的人"},
    {"en": "Toxic Relationships", "zh": "有害的人際關係"},
    {"en": "Trying to Control Others", "zh": "試圖控制他人"},
    {"en": "Expecting Others to Read Your Mind", "zh": "期待他人猜透自己的想法"},
    {"en": "Taking Others for Granted", "zh": "把他人的付出視為理所當然"},
    {"en": "Constant Criticism", "zh": "不斷批評"},
    {"en": "Unnecessary Drama", "zh": "製造不必要的紛爭"},
    {"en": "Comparing Your Journey to Others", "zh": "拿自己的人生與他人比較"},

    # Financial Habits
    {"en": "Impulse Buying", "zh": "衝動消費"},
    {"en": "Overspending", "zh": "過度消費"},
    {"en": "Emotional Spending", "zh": "情緒性消費"},
    {"en": "Unplanned Purchases", "zh": "無計畫購物"},
    {"en": "Ignoring Your Budget", "zh": "忽略預算"},
    {"en": "Lifestyle Inflation", "zh": "生活開銷隨收入增加"},
    {"en": "Buying for Status", "zh": "為了面子而消費"},
    {"en": "Chasing Trends", "zh": "盲目追逐潮流"},
    {"en": "Neglecting Savings", "zh": "忽略儲蓄"},
    {"en": "Avoiding Financial Planning", "zh": "逃避財務規劃"},
    {"en": "Unnecessary Subscriptions", "zh": "不必要的訂閱"},
    {"en": "Fear of Missing Out (FOMO)", "zh": "害怕錯過"},
    {"en": "Comparing Material Possessions", "zh": "比較物質財富"},
    {"en": "Impulse Investing", "zh": "衝動投資"},

    # Decision-Making & Personal Growth
    {"en": "Indecisiveness", "zh": "優柔寡斷"},
    {"en": "Overanalyzing Decisions", "zh": "過度分析決策"},
    {"en": "Fear of Change", "zh": "害怕改變"},
    {"en": "Resistance to Feedback", "zh": "抗拒他人回饋"},
    {"en": "Refusing to Learn", "zh": "拒絕學習"},
    {"en": "Stubbornness", "zh": "固執"},
    {"en": "Blaming Circumstances", "zh": "一味歸咎於環境"},
    {"en": "Avoiding Discomfort", "zh": "逃避不適"},
    {"en": "Fear of Taking Risks", "zh": "害怕承擔風險"},
    {"en": "Giving Up on Goals", "zh": "放棄目標"},
    {"en": "Repeating Old Mistakes", "zh": "重蹈覆轍"},
    {"en": "Ignoring Feedback", "zh": "忽視回饋"},
    {"en": "Unrealistic Comparisons", "zh": "不切實際的比較"},
    {"en": "Living on Autopilot", "zh": "漫無目的地生活"},
    {"en": "Neglecting Personal Goals", "zh": "忽略個人目標"},
    {"en": "Waiting for the Perfect Time", "zh": "等待完美時機"},
    {"en": "Underestimating Yourself", "zh": "低估自己"},
    {"en": "All-or-Nothing Thinking", "zh": "非黑即白的思考"},
    {"en": "Refusing to Ask for Help", "zh": "不願尋求幫助"},
    {"en": "Ignoring Your Values", "zh": "忽視自己的價值觀"},

    # Communication & Behavior
    {"en": "Sarcasm", "zh": "冷嘲熱諷"},
    {"en": "Speaking Without Thinking", "zh": "不經思考便開口"},
    {"en": "Overreacting", "zh": "反應過度"},
    {"en": "Interrupting", "zh": "打斷他人"},
    {"en": "Defensiveness", "zh": "防衛心過強"},
    {"en": "Dishonesty", "zh": "不誠實"},
    {"en": "Exaggeration", "zh": "誇大其詞"},
    {"en": "Breaking Promises", "zh": "不守承諾"},
    {"en": "Avoiding Difficult Conversations", "zh": "逃避艱難的對話"},
    {"en": "Silent Treatment", "zh": "以冷漠對待他人"},
    {"en": "Spreading Rumors", "zh": "散播謠言"},
    {"en": "Being Judgmental", "zh": "習慣評斷他人"},
    {"en": "Unconstructive Criticism", "zh": "缺乏建設性的批評"},
    {"en": "Making Assumptions", "zh": "妄下定論"},
    {"en": "Seeking Revenge", "zh": "尋求報復"},

    # Lifestyle & Mental Clutter
    {"en": "Clutter", "zh": "雜亂"},
    {"en": "Hoarding Unnecessary Things", "zh": "囤積不必要的物品"},
    {"en": "Excessive Noise", "zh": "過度的噪音"},
    {"en": "Constant Notifications", "zh": "不斷跳出的通知"},
    {"en": "Negative News Consumption", "zh": "過度接觸負面新聞"},
    {"en": "Doomscrolling", "zh": "沉迷瀏覽負面資訊"},
    {"en": "Overplanning", "zh": "過度規劃"},
    {"en": "Mental Clutter", "zh": "思緒混亂"},
    {"en": "Unnecessary Stress", "zh": "不必要的壓力"},
    {"en": "Living in the Past", "zh": "活在過去"},
    {"en": "Neglecting the Present", "zh": "忽略當下"},
    {"en": "Constant Busyness", "zh": "總是忙忙碌碌"},
    {"en": "Unhealthy Routines", "zh": "不健康的日常習慣"},
    {"en": "Neglecting Personal Space", "zh": "忽略個人空間"},
    {"en": "Avoiding Silence", "zh": "害怕安靜獨處"},
    {"en": "Unnecessary Commitments", "zh": "不必要的承諾"},
]

QUOTES = [
    # Daily Inspiration
    {
        "en": "An ordinary day can still make an extraordinary you.",
        "zh": "平凡的一天，也能成就很不平凡的你。"
    },
    {
        "en": "Every step you take today brings you closer to your dreams.",
        "zh": "今天邁出的每一步，都在讓你更接近夢想。"
    },
    {
        "en": "Stay curious, stay kind, and let today surprise you.",
        "zh": "保持好奇，保持善良，讓今天為你帶來驚喜。"
    },
    {
        "en": "Peace of mind is the greatest luxury you can gift yourself.",
        "zh": "內心的平靜是你能給予自己最珍貴的禮物。"
    },
    {
        "en": "Small daily improvements over time lead to stunning results.",
        "zh": "微小的日常進步，長久積累必將帶來驚人的成果。"
    },
    {
        "en": "You don't have to be perfect to make a meaningful difference.",
        "zh": "你不需要十全十美，也能創造意義深遠的改變。"
    },
    {
        "en": "Breathe deeply, smile often, and trust the process.",
        "zh": "深呼吸，常微笑，相信時間的力量。"
    },
    {
        "en": "A gentle heart and a brave soul will carry you far.",
        "zh": "溫柔的心靈與勇敢的靈魂將帶你走得更遠。"
    },
    {
        "en": "Light tomorrow with today.",
        "zh": "用今天的努力，照亮明天的路。"
    },
    {
        "en": "Cherish every quiet moment of growth in your life.",
        "zh": "珍惜生命中每一個悄然成長的安靜時刻。"
    },

    # Personal Growth
    {
        "en": "Become a little wiser, kinder, and braver than you were yesterday.",
        "zh": "讓今天的自己比昨天更有智慧、更善良，也更勇敢。"
    },
    {
        "en": "Growth begins when you choose progress over comfort.",
        "zh": "當你選擇進步而非安逸時，成長便開始了。"
    },
    {
        "en": "You are allowed to outgrow the person you used to be.",
        "zh": "你有權超越過去的自己，成為更好的模樣。"
    },
    {
        "en": "Every mistake carries a lesson for a more thoughtful tomorrow.",
        "zh": "每一次錯誤，都藏著讓明天更加成熟的教訓。"
    },
    {
        "en": "Your future is shaped by the choices you repeat today.",
        "zh": "你的未來，由今天反覆做出的選擇塑造。"
    },
    {
        "en": "Be patient with yourself; even mountains rise one layer at a time.",
        "zh": "請對自己多一點耐心，就連高山也是一層層堆積而成。"
    },
    {
        "en": "The courage to begin is already a form of success.",
        "zh": "敢於開始，本身就是一種成功。"
    },
    {
        "en": "You don't need a new life, just a new step in the right direction.",
        "zh": "你不一定需要全新的人生，只需要朝正確的方向再走一步。"
    },
    {
        "en": "Let your experiences teach you, not define you.",
        "zh": "讓經歷教會你成長，而不是決定你是誰。"
    },
    {
        "en": "The best investment is the effort you put into becoming yourself.",
        "zh": "最值得的投資，是努力成為真正的自己。"
    },

    # Mindfulness and Inner Peace
    {
        "en": "You deserve a moment of stillness in a world that never stops.",
        "zh": "在這個永不停歇的世界裡，你值得擁有片刻寧靜。"
    },
    {
        "en": "Not every thought deserves your attention.",
        "zh": "不是每一個念頭，都值得你放在心上。"
    },
    {
        "en": "Let today be lived, not merely rushed through.",
        "zh": "好好感受今天，而不只是匆匆度過今天。"
    },
    {
        "en": "Sometimes the most productive thing you can do is pause.",
        "zh": "有時候，你能做的最有意義的事，就是停下腳步。"
    },
    {
        "en": "Peace grows when you stop fighting what you cannot control.",
        "zh": "當你不再與無法掌控的事情抗爭，內心的平靜便會滋長。"
    },
    {
        "en": "A quiet mind can hear what a busy mind misses.",
        "zh": "安靜的心，才能聽見忙碌的心所忽略的聲音。"
    },
    {
        "en": "Return to your breath whenever life feels overwhelming.",
        "zh": "當生活令人喘不過氣時，就回到自己的呼吸。"
    },
    {
        "en": "You don't have to solve your whole life today.",
        "zh": "你不必在今天就解決人生中的所有問題。"
    },
    {
        "en": "Release the rush; meaningful things take the time they take.",
        "zh": "放下急切，有意義的事情自有其所需的時間。"
    },
    {
        "en": "Stillness is not emptiness; it is room to understand yourself.",
        "zh": "寧靜並非空虛，而是讓你理解自己的空間。"
    },

    # Happiness and Gratitude
    {
        "en": "Happiness often hides inside the moments you almost overlook.",
        "zh": "幸福往往藏在那些差點被你忽略的時刻裡。"
    },
    {
        "en": "Count the little joys, and an ordinary day becomes abundant.",
        "zh": "數一數生活中的小確幸，平凡的一天也會變得豐盛。"
    },
    {
        "en": "Gratitude turns what you have into something wonderful.",
        "zh": "感恩能讓你已經擁有的一切變得更加美好。"
    },
    {
        "en": "You can have an imperfect day and still find something beautiful in it.",
        "zh": "即使今天並不完美，你依然能在其中找到美好。"
    },
    {
        "en": "Joy doesn't always arrive loudly; sometimes it whispers.",
        "zh": "喜悅不一定轟轟烈烈地到來，有時它只是輕聲細語。"
    },
    {
        "en": "A grateful heart makes room for more wonder.",
        "zh": "懂得感恩的心，能容納更多生活中的驚喜。"
    },
    {
        "en": "You don't need everything to be happy with something.",
        "zh": "你不必擁有一切，才能為已擁有的事物感到幸福。"
    },
    {
        "en": "Let yourself enjoy the good without waiting for the perfect.",
        "zh": "別再等待完美，現在就允許自己享受美好。"
    },
    {
        "en": "Some of life's richest moments cost nothing at all.",
        "zh": "人生中最珍貴的一些時刻，往往分文不花。"
    },
    {
        "en": "Notice what is going right, even while you work on what isn't.",
        "zh": "即使正在改善不足之處，也別忘了看見那些正在變好的事情。"
    },

    # Kindness and Relationships
    {
        "en": "Kindness is a small act that can leave a lasting echo.",
        "zh": "善意雖是微小的舉動，卻能留下長久的回響。"
    },
    {
        "en": "Listen to understand, not merely to prepare your reply.",
        "zh": "傾聽是為了理解，而不只是為了準備回答。"
    },
    {
        "en": "A little patience can protect a relationship from a thousand regrets.",
        "zh": "多一點耐心，或許就能避免無數令人後悔的時刻。"
    },
    {
        "en": "Make people feel seen, heard, and valued.",
        "zh": "讓身邊的人感受到被看見、被聆聽與被珍惜。"
    },
    {
        "en": "You can be kind without abandoning your boundaries.",
        "zh": "你可以保持善良，同時堅守自己的界線。"
    },
    {
        "en": "A sincere apology can open a door that pride keeps closed.",
        "zh": "真誠的道歉，能打開自尊與驕傲所緊閉的門。"
    },
    {
        "en": "The smallest thoughtful gesture can brighten someone's hardest day.",
        "zh": "一個小小的貼心舉動，就能照亮某人最艱難的一天。"
    },
    {
        "en": "Choose connection over the need to be right.",
        "zh": "選擇維繫彼此的連結，而不是一味堅持自己正確。"
    },
    {
        "en": "Respect is kindness that continues even when opinions differ.",
        "zh": "即使意見不同，依然願意尊重彼此，便是持續的善意。"
    },
    {
        "en": "Be the reason someone feels a little less alone today.",
        "zh": "成為那個讓某人在今天感到不再那麼孤單的人。"
    },

    # Resilience and Courage
    {
        "en": "A difficult chapter does not make a difficult life.",
        "zh": "人生中的艱難篇章，不代表整個人生都會艱難。"
    },
    {
        "en": "You can be afraid and still take the next step.",
        "zh": "即使心懷恐懼，你依然可以邁出下一步。"
    },
    {
        "en": "Rest when you need to, but don't mistake rest for giving up.",
        "zh": "需要時就休息，但別把休息誤認為放棄。"
    },
    {
        "en": "Your setbacks can become part of the wisdom you carry forward.",
        "zh": "挫折也能成為你帶著繼續前行的智慧。"
    },
    {
        "en": "You have survived days you once thought you couldn't face.",
        "zh": "你已經走過那些曾讓你覺得難以承受的日子。"
    },
    {
        "en": "Bravery is choosing what matters while uncertainty remains.",
        "zh": "勇敢是在不確定依然存在時，仍選擇對自己重要的事。"
    },
    {
        "en": "One setback cannot erase all the progress that came before it.",
        "zh": "一次挫折，無法抹去你此前所有的努力與進步。"
    },
    {
        "en": "You are allowed to start again without calling yourself a failure.",
        "zh": "你可以重新開始，而不必因此把自己視為失敗者。"
    },
    {
        "en": "Strength sometimes looks like asking for help.",
        "zh": "有時候，勇敢堅強的表現就是主動尋求幫助。"
    },
    {
        "en": "Even slow progress is movement toward something better.",
        "zh": "即使進步緩慢，也依然是在朝更好的方向前進。"
    },

    # Productivity and Discipline
    {
        "en": "Start before you feel ready; clarity often follows action.",
        "zh": "在覺得自己準備好之前就開始，清晰的方向往往來自行動。"
    },
    {
        "en": "Protect your attention as carefully as you protect your time.",
        "zh": "像珍惜時間一樣，謹慎守護自己的注意力。"
    },
    {
        "en": "A focused hour can be more valuable than a distracted day.",
        "zh": "專注的一小時，可能勝過分心的一整天。"
    },
    {
        "en": "Make the next step small enough that you can begin now.",
        "zh": "把下一步縮小到足以讓你現在就開始。"
    },
    {
        "en": "Consistency quietly accomplishes what occasional intensity cannot.",
        "zh": "持之以恆能悄悄完成許多一時熱情無法做到的事。"
    },
    {
        "en": "You don't need to do everything; you need to do what matters.",
        "zh": "你不必完成所有事情，只需做好真正重要的事。"
    },
    {
        "en": "Every promise you keep to yourself builds self-trust.",
        "zh": "每一次信守對自己的承諾，都在累積對自己的信任。"
    },
    {
        "en": "Progress becomes visible after effort has been repeated long enough.",
        "zh": "當努力持續累積到一定程度，進步自然會逐漸顯現。"
    },
    {
        "en": "Finish one meaningful thing before chasing ten new ones.",
        "zh": "在追逐十件新事情之前，先完成一件真正有意義的事。"
    },
    {
        "en": "Your daily habits are votes for the future you want.",
        "zh": "你的日常習慣，每一天都在為你想要的未來投票。"
    },

    # Self-Love and Self-Care
    {
        "en": "Speak to yourself with the same kindness you offer a friend.",
        "zh": "用你對待朋友的善意，好好對待自己。"
    },
    {
        "en": "Your worth does not rise and fall with your productivity.",
        "zh": "你的價值不會隨著工作效率的高低而增減。"
    },
    {
        "en": "You are a person to care for, not a project to perfect.",
        "zh": "你是一個值得被照顧的人，而不是一個必須被完善的計畫。"
    },
    {
        "en": "Rest is part of a meaningful life, not a reward for exhaustion.",
        "zh": "休息是有意義生活的一部分，而不是筋疲力盡後才能獲得的獎勵。"
    },
    {
        "en": "You can honor your limits without surrendering your dreams.",
        "zh": "你可以尊重自己的極限，同時不放棄夢想。"
    },
    {
        "en": "Give yourself permission to be a work in progress.",
        "zh": "允許自己持續成長，不必急著成為完美的人。"
    },
    {
        "en": "You deserve the care you keep giving to everyone else.",
        "zh": "你也值得獲得那些你一直給予他人的關懷。"
    },
    {
        "en": "Let go of the need to earn your right to rest.",
        "zh": "放下那種必須先證明自己有所成就，才有資格休息的想法。"
    },
    {
        "en": "Your pace is valid, even when it differs from everyone else's.",
        "zh": "即使你的步調與他人不同，它依然值得被尊重。"
    },
    {
        "en": "Taking care of yourself helps you show up more fully for life.",
        "zh": "好好照顧自己，能讓你更有力量地投入生活。"
    },

    # Creativity and Curiosity
    {
        "en": "Ask one more question, and the world may open a new door.",
        "zh": "再多問一個問題，世界或許就會為你開啟一扇新門。"
    },
    {
        "en": "You don't need permission to explore a new possibility.",
        "zh": "探索新的可能性，不需要等待別人的許可。"
    },
    {
        "en": "Every beginner was once brave enough to be inexperienced.",
        "zh": "每一位初學者，都曾勇敢地接受自己的生疏。"
    },
    {
        "en": "Curiosity turns ordinary routines into opportunities to discover.",
        "zh": "好奇心能把平凡的日常，變成探索新事物的機會。"
    },
    {
        "en": "Create something imperfect rather than imagine something forever.",
        "zh": "與其永遠停留在想像，不如創造一些不完美的作品。"
    },
    {
        "en": "A different perspective can reveal a possibility you couldn't see before.",
        "zh": "換個角度思考，就可能看見過去未曾發現的可能。"
    },
    {
        "en": "Let questions lead you where assumptions never could.",
        "zh": "讓問題引領你前往那些既有假設無法帶你抵達的地方。"
    },
    {
        "en": "Play, experiment, and give your imagination room to breathe.",
        "zh": "盡情玩耍、勇於嘗試，讓想像力自由舒展。"
    },
    {
        "en": "You can learn something valuable from an unexpected place.",
        "zh": "你總能從意想不到的地方學到有價值的事物。"
    },
    {
        "en": "Wonder is the beginning of many beautiful discoveries.",
        "zh": "心懷驚奇，是許多美好發現的起點。"
    },

    # Purpose and Meaning
    {
        "en": "A meaningful life is built through meaningful ordinary moments.",
        "zh": "有意義的人生，是由一個個有意義的平凡時刻組成的。"
    },
    {
        "en": "Let your values guide you when the path becomes unclear.",
        "zh": "當前方的道路變得模糊時，讓你的價值觀指引方向。"
    },
    {
        "en": "Success feels richer when it reflects who you truly are.",
        "zh": "當成功體現了真實的自己，它才會帶來更深刻的滿足。"
    },
    {
        "en": "You can change direction without losing the wisdom of your journey.",
        "zh": "你可以改變方向，而不會失去一路走來累積的智慧。"
    },
    {
        "en": "Make room for the things you want your life to stand for.",
        "zh": "為那些代表你人生價值的事物，留出足夠的空間。"
    },
    {
        "en": "A good life is not only about reaching places, but noticing the journey.",
        "zh": "美好的人生不只是抵達目的地，也在於感受沿途的風景。"
    },
    {
        "en": "Let your actions reflect the person you hope to become.",
        "zh": "讓你的行動，展現你希望成為的那個人。"
    },
    {
        "en": "You don't have to change the whole world to make your part matter.",
        "zh": "你不必改變整個世界，才能讓自己的付出具有意義。"
    },
    {
        "en": "Choose what makes your life feel honest, not merely impressive.",
        "zh": "選擇讓自己活得真誠的事，而不只是讓別人覺得你很出色的事。"
    },
    {
        "en": "Build a life that feels good from the inside, not just one that looks good outside.",
        "zh": "打造一個由內而外都讓自己感到美好的生活，而不只是看起來光鮮亮麗的人生。"
    },
]

LUCKY_COLORS = [
    {"name_en": "Pink", "name_zh": "粉色", "hex": "#FF69B4"},
    {"name_en": "Gold", "name_zh": "金色", "hex": "#FFD700"},
    {"name_en": "Emerald Green", "name_zh": "翠綠", "hex": "#50C878"},
    {"name_en": "Sky Blue", "name_zh": "天藍", "hex": "#87CEEB"},
    {"name_en": "Lavender Purple", "name_zh": "薰衣草紫", "hex": "#E6E6FA"},
    {"name_en": "Coral Orange", "name_zh": "珊瑚橘", "hex": "#FF7F50"},
    {"name_en": "Mint Green", "name_zh": "薄荷綠", "hex": "#98FF98"},
    {"name_en": "Cream Yellow", "name_zh": "奶黃", "hex": "#FFFDD0"},
    {"name_en": "Rose Red", "name_zh": "玫瑰紅", "hex": "#C21E56"},
    {"name_en": "Silver White", "name_zh": "銀白", "hex": "#C0C0C0"},
    {"name_en": "Ocean Blue", "name_zh": "海洋藍", "hex": "#006994"},
    {"name_en": "Royal Blue", "name_zh": "寶藍", "hex": "#4169E1"},
    {"name_en": "Turquoise", "name_zh": "綠松石藍", "hex": "#40E0D0"},
    {"name_en": "Teal", "name_zh": "藍綠色", "hex": "#008080"},
    {"name_en": "Navy Blue", "name_zh": "海軍藍", "hex": "#000080"},
    {"name_en": "Baby Blue", "name_zh": "嬰兒藍", "hex": "#89CFF0"},
    {"name_en": "Ice Blue", "name_zh": "冰藍", "hex": "#D6F1FF"},
    {"name_en": "Sapphire Blue", "name_zh": "藍寶石藍", "hex": "#0F52BA"},
    {"name_en": "Midnight Blue", "name_zh": "午夜藍", "hex": "#191970"},
    {"name_en": "Periwinkle", "name_zh": "長春花藍", "hex": "#CCCCFF"},
    {"name_en": "Indigo", "name_zh": "靛藍", "hex": "#4B0082"},
    {"name_en": "Lilac", "name_zh": "丁香紫", "hex": "#C8A2C8"},
    {"name_en": "Mauve", "name_zh": "藕紫色", "hex": "#E0B0FF"},
    {"name_en": "Plum Purple", "name_zh": "梅紫", "hex": "#8E4585"},
    {"name_en": "Amethyst", "name_zh": "紫水晶色", "hex": "#9966CC"},
    {"name_en": "Orchid", "name_zh": "蘭花紫", "hex": "#DA70D6"},
    {"name_en": "Burgundy", "name_zh": "酒紅", "hex": "#800020"},
    {"name_en": "Crimson Red", "name_zh": "緋紅", "hex": "#DC143C"},
    {"name_en": "Ruby Red", "name_zh": "紅寶石紅", "hex": "#E0115F"},
    {"name_en": "Cherry Red", "name_zh": "櫻桃紅", "hex": "#D2042D"},
    {"name_en": "Scarlet", "name_zh": "猩紅", "hex": "#FF2400"},
    {"name_en": "Brick Red", "name_zh": "磚紅", "hex": "#CB4154"},
    {"name_en": "Salmon Pink", "name_zh": "鮭魚粉", "hex": "#FA8072"},
    {"name_en": "Blush Pink", "name_zh": "淡粉紅", "hex": "#DE5D83"},
    {"name_en": "Dusty Rose", "name_zh": "灰玫瑰色", "hex": "#DCAE96"},
    {"name_en": "Peach", "name_zh": "蜜桃色", "hex": "#FFCBA4"},
    {"name_en": "Apricot", "name_zh": "杏色", "hex": "#FBCEB1"},
    {"name_en": "Champagne", "name_zh": "香檳色", "hex": "#F7E7CE"},
    {"name_en": "Rose Gold", "name_zh": "玫瑰金", "hex": "#B76E79"},
    {"name_en": "Copper", "name_zh": "銅色", "hex": "#B87333"},
    {"name_en": "Bronze", "name_zh": "青銅色", "hex": "#CD7F32"},
    {"name_en": "Amber", "name_zh": "琥珀色", "hex": "#FFBF00"},
    {"name_en": "Mustard Yellow", "name_zh": "芥末黃", "hex": "#FFDB58"},
    {"name_en": "Lemon Yellow", "name_zh": "檸檬黃", "hex": "#FFF44F"},
    {"name_en": "Butter Yellow", "name_zh": "奶油黃", "hex": "#FFEDA0"},
    {"name_en": "Honey Gold", "name_zh": "蜂蜜金", "hex": "#EB9605"},
    {"name_en": "Saffron", "name_zh": "藏紅花黃", "hex": "#F4C430"},
    {"name_en": "Olive Green", "name_zh": "橄欖綠", "hex": "#808000"},
    {"name_en": "Sage Green", "name_zh": "鼠尾草綠", "hex": "#9CAF88"},
    {"name_en": "Forest Green", "name_zh": "森林綠", "hex": "#228B22"},
    {"name_en": "Jade Green", "name_zh": "翡翠綠", "hex": "#00A86B"},
    {"name_en": "Pistachio Green", "name_zh": "開心果綠", "hex": "#93C572"},
    {"name_en": "Seafoam Green", "name_zh": "海沫綠", "hex": "#9FE2BF"},
    {"name_en": "Lime Green", "name_zh": "萊姆綠", "hex": "#32CD32"},
    {"name_en": "Moss Green", "name_zh": "苔蘚綠", "hex": "#8A9A5B"},
    {"name_en": "Pine Green", "name_zh": "松綠", "hex": "#01796F"},
    {"name_en": "Hunter Green", "name_zh": "獵人綠", "hex": "#355E3B"},
    {"name_en": "Chartreuse", "name_zh": "黃綠色", "hex": "#7FFF00"},
    {"name_en": "Cobalt Blue", "name_zh": "鈷藍", "hex": "#0047AB"},
    {"name_en": "Steel Blue", "name_zh": "鋼藍", "hex": "#4682B4"},
    {"name_en": "Denim Blue", "name_zh": "牛仔藍", "hex": "#1560BD"},
    {"name_en": "Powder Blue", "name_zh": "粉藍", "hex": "#B0E0E6"},
    {"name_en": "Slate Blue", "name_zh": "石板藍", "hex": "#6A5ACD"},
    {"name_en": "Aqua", "name_zh": "水藍色", "hex": "#00FFFF"},
    {"name_en": "Ice Lavender", "name_zh": "冰薰衣草紫", "hex": "#E6E6FA"},
    {"name_en": "Charcoal Gray", "name_zh": "炭灰色", "hex": "#36454F"},
    {"name_en": "Slate Gray", "name_zh": "石板灰", "hex": "#708090"},
    {"name_en": "Pearl White", "name_zh": "珍珠白", "hex": "#F8F6F0"},
    {"name_en": "Ivory", "name_zh": "象牙白", "hex": "#FFFFF0"},
    {"name_en": "Snow White", "name_zh": "雪白", "hex": "#FFFAFA"},
    {"name_en": "Beige", "name_zh": "米色", "hex": "#F5F5DC"},
    {"name_en": "Taupe", "name_zh": "灰褐色", "hex": "#483C32"},
    {"name_en": "Chocolate Brown", "name_zh": "巧克力棕", "hex": "#7B3F00"},
    {"name_en": "Caramel", "name_zh": "焦糖色", "hex": "#C68E17"},
    {"name_en": "Cinnamon", "name_zh": "肉桂色", "hex": "#D2691E"},
    {"name_en": "Terracotta", "name_zh": "陶土色", "hex": "#E2725B"},
    {"name_en": "Burnt Orange", "name_zh": "焦橘色", "hex": "#CC5500"},
    {"name_en": "Tangerine", "name_zh": "橘子色", "hex": "#F28500"},
    {"name_en": "Pumpkin Orange", "name_zh": "南瓜橘", "hex": "#FF7518"},
    {"name_en": "Rust Orange", "name_zh": "鐵鏽橘", "hex": "#B7410E"},
    {"name_en": "Magenta", "name_zh": "洋紅色", "hex": "#FF00FF"},
    {"name_en": "Fuchsia", "name_zh": "紫紅色", "hex": "#FF00FF"},
    {"name_en": "Coral Pink", "name_zh": "珊瑚粉", "hex": "#F88379"},
    {"name_en": "Watermelon Pink", "name_zh": "西瓜粉", "hex": "#FC6C85"},
    {"name_en": "Cotton Candy", "name_zh": "棉花糖粉", "hex": "#FFB7D5"},
    {"name_en": "Vanilla Cream", "name_zh": "香草奶油色", "hex": "#F3E5AB"},
    {"name_en": "Lemon Cream", "name_zh": "檸檬奶油色", "hex": "#FFFACD"},
    {"name_en": "Sea Glass", "name_zh": "海玻璃綠", "hex": "#A7C7B7"},
    {"name_en": "Eucalyptus Green", "name_zh": "尤加利綠", "hex": "#7A9E7E"},
    {"name_en": "Celadon", "name_zh": "青瓷綠", "hex": "#ACE1AF"},
    {"name_en": "Malachite Green", "name_zh": "孔雀石綠", "hex": "#0BDA51"},
    {"name_en": "Viridian", "name_zh": "鉻綠", "hex": "#40826D"},
    {"name_en": "Aubergine", "name_zh": "茄紫色", "hex": "#614051"},
    {"name_en": "Mulberry", "name_zh": "桑葚紫", "hex": "#C54B8C"},
    {"name_en": "Wisteria", "name_zh": "紫藤色", "hex": "#C9A0DC"},
    {"name_en": "Smoky Purple", "name_zh": "煙紫色", "hex": "#A087A6"},
    {"name_en": "Antique Gold", "name_zh": "古金色", "hex": "#C9A227"},
    {"name_en": "Pale Gold", "name_zh": "淡金色", "hex": "#E6BE8A"},
    {"name_en": "Platinum", "name_zh": "鉑金色", "hex": "#E5E4E2"},
    {"name_en": "Graphite Gray", "name_zh": "石墨灰", "hex": "#474A51"},
]

LUCKY_DIRECTIONS = [
    {"code": "N", "name_en": "North", "name_zh": "正北"},
    {"code": "NBE", "name_en": "North by East", "name_zh": "北偏東微東"},
    {"code": "NNE", "name_en": "North-Northeast", "name_zh": "北東北"},
    {"code": "NEBN", "name_en": "Northeast by North", "name_zh": "東北偏北"},
    {"code": "NE", "name_en": "Northeast", "name_zh": "東北"},
    {"code": "NEBE", "name_en": "Northeast by East", "name_zh": "東北偏東"},
    {"code": "ENE", "name_en": "East-Northeast", "name_zh": "東北東"},
    {"code": "EBN", "name_en": "East by North", "name_zh": "東偏北微北"},
    {"code": "E", "name_en": "East", "name_zh": "正東"},
    {"code": "EBS", "name_en": "East by South", "name_zh": "東偏南微南"},
    {"code": "ESE", "name_en": "East-Southeast", "name_zh": "東南東"},
    {"code": "SEBE", "name_en": "Southeast by East", "name_zh": "東南偏東"},
    {"code": "SE", "name_en": "Southeast", "name_zh": "東南"},
    {"code": "SEBS", "name_en": "Southeast by South", "name_zh": "東南偏南"},
    {"code": "SSE", "name_en": "South-Southeast", "name_zh": "南南東"},
    {"code": "SBE", "name_en": "South by East", "name_zh": "南偏東微東"},
    {"code": "S", "name_en": "South", "name_zh": "正南"},
    {"code": "SBW", "name_en": "South by West", "name_zh": "南偏西微西"},
    {"code": "SSW", "name_en": "South-Southwest", "name_zh": "南南西"},
    {"code": "SWBS", "name_en": "Southwest by South", "name_zh": "西南偏南"},
    {"code": "SW", "name_en": "Southwest", "name_zh": "西南"},
    {"code": "SWBW", "name_en": "Southwest by West", "name_zh": "西南偏西"},
    {"code": "WSW", "name_en": "West-Southwest", "name_zh": "西南西"},
    {"code": "WBS", "name_en": "West by South", "name_zh": "西偏南微南"},
    {"code": "W", "name_en": "West", "name_zh": "正西"},
    {"code": "WBN", "name_en": "West by North", "name_zh": "西偏北微北"},
    {"code": "WNW", "name_en": "West-Northwest", "name_zh": "西北西"},
    {"code": "NWBW", "name_en": "Northwest by West", "name_zh": "西北偏西"},
    {"code": "NW", "name_en": "Northwest", "name_zh": "西北"},
    {"code": "NWBN", "name_en": "Northwest by North", "name_zh": "西北偏北"},
    {"code": "NNW", "name_en": "North-Northwest", "name_zh": "北北西"},
    {"code": "NBW", "name_en": "North by West", "name_zh": "北偏西微西"},
]


def get_all_choices():
    """
    Returns the comprehensive dictionary of all pre-defined choices
    so the user or frontend can inspect and enrich the pool.
    """
    return {
        "good_for_choices": GOOD_FOR_CHOICES,
        "avoid_choices": AVOID_CHOICES,
        "quotes": QUOTES,
        "lucky_colors": LUCKY_COLORS,
        "lucky_directions": LUCKY_DIRECTIONS,
        "lucky_number_range": {"min": 1, "max": 99},
    }


def generate_random_daily_fortune():
    """
    Randomly chooses a set of daily fortune data matching the 'Today's Cat' card.
    """
    selected_good = random.sample(GOOD_FOR_CHOICES, min(3, len(GOOD_FOR_CHOICES)))
    selected_avoid = random.sample(AVOID_CHOICES, min(3, len(AVOID_CHOICES)))
    selected_quote = random.choice(QUOTES)
    selected_color = random.choice(LUCKY_COLORS)
    selected_direction = random.choice(LUCKY_DIRECTIONS)
    selected_number = random.randint(1, 99)

    return {
        "good_for": {
            "en": ", ".join([item["en"] for item in selected_good]),
            "zh": "、".join([item["zh"] for item in selected_good]),
            "items_en": [item["en"] for item in selected_good],
            "items_zh": [item["zh"] for item in selected_good],
        },
        "avoid": {
            "en": ", ".join([item["en"] for item in selected_avoid]),
            "zh": "、".join([item["zh"] for item in selected_avoid]),
            "items_en": [item["en"] for item in selected_avoid],
            "items_zh": [item["zh"] for item in selected_avoid],
        },
        "quote": selected_quote,
        "lucky_color": selected_color,
        "lucky_direction": selected_direction,
        "lucky_number": selected_number,
    }


generate_random_daily_check_in = generate_random_daily_fortune

