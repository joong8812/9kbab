# 9k밥 (9kbab) 🍲

## 1. 설명
9천원 이하의 가성비 맛집 정보를 공유하는 SNS (모바일 최적화)   
http://beloved-coder.shop/

시연영상: https://youtu.be/sanaSKuFWZI


## 2. 팀 구성
* 박다희: 프론트엔드, 디자인 [<img src="https://img.shields.io/badge/Github-181717?style=flat-square&logo=Github&logoColor=white"/></a>](https://github.com/Dahee0628)
* 정유진: 프론트엔드, 디자인 [<img src="https://img.shields.io/badge/Github-181717?style=flat-square&logo=Github&logoColor=white"/></a>](https://github.com/Augustj88)
* 고희석: 백엔드, API설계 [<img src="https://img.shields.io/badge/Github-181717?style=flat-square&logo=Github&logoColor=white"/></a>](https://github.com/GoHeeSeok00)
* 정기홍: 백엔드, 테스트 [<img src="https://img.shields.io/badge/Github-181717?style=flat-square&logo=Github&logoColor=white"/></a>](https://github.com/ghj99)
* 최중재: 팀장, EC2 [<img src="https://img.shields.io/badge/Github-181717?style=flat-square&logo=Github&logoColor=white"/></a>](https://github.com/joong8812)

## 3. 기술
<img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=HTML5&logoColor=white"/></a>
<img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=CSS3&logoColor=white"/></a>
<img src="https://img.shields.io/badge/Javascript-F7DF1E?style=flat-square&logo=Javascript&logoColor=white"/></a>
<img src="https://img.shields.io/badge/JQuery-0769AD?style=flat-square&logo=JQuery&logoColor=white"/></a>
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/></a>
<img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=Flask&logoColor=white"/></a>
<img src="https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=MongoDB&logoColor=white"/></a>
<img src="https://img.shields.io/badge/Amazon AWS-232F3E?style=flat-square&logo=Amazon AWS&logoColor=white"/></a>

## 4. 와이어프레임

<img src="./attached/9kbab-wireframe.jpg" alt="wireframe">

## 5. API 설계

| 기능 | 세부 | Method | URL | request | response |
| --- | --- | --- | --- | --- | --- |
| 회원가입 | 아이디, 패스워드 ,닉네임 등록 | POST | /signup | {’userid’:userid, ’email’:email, ‘password’:password, ‘nickname’:nickname} | DB 저장 YES or NO |
| 로그인 |  | POST | /login | {’email’:email, ‘password’:password | DB  select YES or NO |
| 메인페이지 |  | GET | /mainfeed |  | 전체 피드 리스트 |
| 프로필 편집 |  | PUT(POST) | /profile(/edit) | {’photo’:photo, ‘nickname’:nickname,’introduce’:introduce} | DB 수정 YES or NO |
| 글 작성 |  | POST | /post | {’photo’:photo, ‘writing’: writing, ‘location’:location’, ‘tag’:tag} | DB 저장 YES or NO  |
| 글 편집 |  | PUT(POST) | /post(/edit) | {’photo’:photo, ‘writing’:writing, ‘location’:location’, ‘tag’:tag} | DB 수정 YES or NO  |
| 글 삭제 |  | DELETE(POST) | /post(/delete) | {’postid’:postid} | DB 삭제 YES or NO  |
| 내 피드 불러오기 |  | POST | /myfeed | {’userid’:userid} | 전체 나의 피드 리스트 |
| 내 피드 삭제하기 |  | DELETE(POST) | /myfeed(/delete) | {’postid’:postid} | DB 삭제 YES or NO  |
| 마이페이지 |  | POST | /mypage | {’nickname’:nickname} | 프로필 정보, 나의 피드 리스트 |
| 댓글 페이지 |  | GET | /post/:id/comment | id={게시글 넘버} | 해당 게시글 댓글 리스트 |
| 좋아요 | 게시글 좋아요 카운트 | GET | /post/:id/like | id={게시글 넘버} | 해당 게시글 좋아요 카운트 |
| 좋아요 | like 생성 | PUT(POST) | /post/:id/like | {’postid’:postid, ‘userid’:userid} | DB update YES or NO  |
| 댓글 |  | POST | /post/:id/comment | {’comment’:comment, ‘postid’: postid, ‘userid’:userid} | DB 저장 YES or NO |
