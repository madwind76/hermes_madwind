---
title: Volatility 3를 이용한 메모리 적재 보안 로그 삭제 탐지 (Memory Event Log Service Audit)
created: 2026-06-28
updated: 2026-06-28
type: ctf-challenge
tags: [ctf, ctf-challenge, forensics, memory, volatility, event-log, evtx, eventlog-service, log-clearing]
confidence: high
---

# Volatility 3를 이용한 메모리 적재 보안 로그 삭제 탐지 (Memory Event Log Service Audit)

> **난이도**: 초중급  
> **소요 시간**: 25~30분  
> **참고 picoCTF 문제**: 메모리 상의 이벤트 로그 서비스 감사 기록 복구 (Volatility Eventlog Mem Carving)

## 1. 배경 시나리오
지능형 지속 위협(APT) 공격자가 도메인 컨트롤러 시스템 내부에서 관리자 계정 횡적 이동(Lateral Movement) 흔적을 은닉하기 위해 윈도우 기본 도구인 `wevtutil.exe`를 사용하여 보안(Security) 이벤트 로그를 강제로 초기화 및 삭제(`wevtutil cl Security`)했습니다. 디스크 상의 `Security.evtx` 파일 내부 레코드가 전부 소거되어 감사 추적이 불가능해진 직후, 다행히도 해당 서버의 가동 중인 RAM 메모리 덤프가 수집 보존되었습니다. 윈도우의 이벤트 로그 관리 데몬 서비스인 **eventlog** (공유 `svchost.exe` 프로세스로 기동)는 동작 중 생성/처리되는 이벤트 레코드들을 디스크에 저장하기 직전 커널 메모리 페이지 풀(Page Pool) 버퍼에 일시 적재하여 연산합니다. 수집한 eventlog 프로세스의 가상 메모리 덤프 텍스트 리포트인 `eventlog_mem_dump.txt`를 정밀 스캔하여, **삭제 명령 직전 메모리 버퍼 상에 기표 잔재되어 남아있던 보안 감사 레코드 속의 플래그**를 구출하십시오.

## 2. 제공 파일
* `eventlog_mem_dump.txt` (이벤트 로그 서비스 프로세스 가상 메모리 대역을 Volatility 3로 덤프하여 문자열 구조를 정제 추출한 텍스트 파일)

## 3. 문제 목표
윈도우 이벤트 로그 감사 서비스(`eventlog`)가 실행 중 메모리에 적재 보존하는 이벤트 청크 구조(특히 **Event ID 1102 - The audit log was cleared** 또는 마지막 처리 중이던 이벤트 레코드 XML 데이터 버퍼)를 이해하고, 메모리 덤프에서 평문 잔재 필드를 복원해 냅니다.

## 4. 의도한 풀이 흐름
1. **메모리 적재 텍스트 레코드 검색**:
   * 제공된 `eventlog_mem_dump.txt` 파일을 텍스트 에디터로 엽니다.
   * 파일 내부에 잔재하는 이벤트 로그 XML 기표 흔적이나 특정 키워드를 검색합니다.
     `grep "picoCTF" eventlog_mem_dump.txt`
2. **이벤트 서비스 가상 버퍼 해독**:
   * 스캔 결과, eventlog 서비스 프로세스가 메모리 힙 버퍼에 캐싱하고 있던 마지막 XML 레코드 중 이벤트 감사 로그가 클리어되었음을 스스로 기표한 **Event ID 1102** 레코드 정보 영역을 포착합니다:
     ```xml
     <Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
       <System>
         <Provider Name="Microsoft-Windows-Eventlog" Guid="{fc65c3b3-e18e-4516-a85f-83d81d17a996}"/>
         <EventID>1102</EventID>
         <Version>0</Version>
         <Level>4</Level>
         <Task>104</Task>
         <Opcode>0</Opcode>
         <Keywords>0x8020000000000000</Keywords>
         <TimeCreated SystemTime="2026-06-28T10:45:15.123456Z"/>
         <EventRecordID>1045</EventRecordID>
         <Correlation/>
         <Execution ProcessID="104" ThreadID="884"/>
         <Channel>Security</Channel>
         <Computer>DC.CONTOSO.LOCAL</Computer>
         <Security/>
       </System>
       <UserData>
         <LogFileCleared xmlns="http://manifests.microsoft.com/win/2004/08/windows/eventlog">
           <SubjectUserSid>S-1-5-21-12345678-87654321-12345678-500</SubjectUserSid>
           <SubjectUserName>Administrator</SubjectUserName>
           <SubjectDomainName>CONTOSO</SubjectDomainName>
           <SubjectLogonId>0x3e7</SubjectLogonId>
           <ExtraInfo>picoCTF{eventl0g_service_mem_carved_r3cords}</ExtraInfo>
         </LogFileCleared>
       </UserData>
     </Event>
     ```
3. **플래그 도출**:
   * `ExtraInfo` 노드 매개변수 데이터 영역에 하드코딩 형태로 남은 최종 플래그 값을 획득합니다:
     `picoCTF{eventl0g_service_mem_carved_r3cords}`

## 5. 정답(플래그) 규칙 및 예시
* **플래그 형식**: `picoCTF{<flag_string>}`
* **예시**: `picoCTF{eventl0g_service_mem_carved_r3cords}`

## 6. 출제자 노트 & 파일 제작 가이드
* **아티팩트 제작 방법**:
  1. Windows 가상 머신 환경에서 관리자 권한 명령창을 열고 보안 이벤트를 강제 소거합니다:
     `wevtutil cl Security`
     (이때 이벤트 로그 서비스 엔진이 내부 시스템 메타데이터 갱신 및 Event ID 1102 레코드를 처리하여 런타임 메모리 버퍼에 할당 적재합니다)
  2. 즉시 OS 물리 메모리 덤프를 생성합니다.
  3. Volatility 3 프레임워크를 구동하여 이벤트 로그 서비스(`eventlog`)가 실행 중인 `svchost.exe` 프로세스의 PID를 식별합니다:
     `python3 vol.py -f memory.raw windows.pslist`
  4. 해당 PID를 인자로 전달하여 가상 메모리 세그먼트 전체를 덤프 획득합니다:
     `python3 vol.py -f memory.raw windows.memmap --pid <eventlog_PID> --dump`
  5. 덤프 파일 내에서 XML 이벤트 구조와 플래그 정보를 필터 분석한 뒤 유의미한 감사 세그먼트 대역을 `eventlog_mem_dump.txt` 파일로 구성해 수검자에게 배포합니다.
* **출제 포인트**: 
  * 침해 위협 피의자가 디스크 기반 로그를 무력화하는 안티 포렌식 공격(Event Log Cleared)을 수행했더라도, 활성 메모리 상에 상주 기동 중인 OS 감사 데몬의 가상 프로세스 메모리 버퍼(Eventlog Service Process Memory Forensics)를 덤프해 마지막 삭제 정황 증적을 성공적으로 환원 및 입증하는 능력을 검증합니다.

## 7. 트러블슈팅 및 힌트
* **Q. 이벤트 로그 삭제 시 기록되는 Event ID 1102는 Security 로그 외에 다른 채널에도 기표되나요?**
  * A. `Event ID 1102` (The audit log was cleared) 감사 정책은 오직 **보안(Security)** 이벤트 로그 채널이 비워질 때만 해당 시스템에 자동으로 수집 및 기록됩니다. 만약 시스템(System) 또는 애플리케이션(Application) 로그 채널이 초기화된 경우에는 해당 채널 정보 영역에 **Event ID 104** (System Log Cleared) 감사 레코드가 별도로 수립되어 남게 되므로, 삭제 대상 채널의 종별에 따라 이벤트 ID 타깃을 1102 혹은 104로 구분해서 교차 필터링해야 올바른 원인을 규명할 수 있습니다.
* **Q. eventlog 서비스가 돌고 있는 svchost.exe 프로세스는 어떻게 쉽게 가려내나요?**
  * A. 윈도우는 여러 대외 서비스를 단일 `svchost.exe`에 공유 결합하여 실행하므로 프로세스 이름만으로는 식별이 불가능합니다. Volatility의 `windows.pstree`나 `windows.info`를 구동하거나, `tasklist /svc` 기법을 모사하여 해당 svchost 프로세스가 호스팅하는 서비스 명칭 목록 중 `eventlog` 태그가 바인딩된 인스턴스의 PID를 찾아 매핑하는 단계를 선행해야 합니다.

## 8. 학습 포인트
* **윈도우 이벤트 로그 수집 아키텍처**: 커널 이벤트 채널 처리 구조 및 서비스 메모리 페이지 풀 버퍼 캐싱 메커니즘을 상세히 이해합니다.
* **안티 포렌식 무력화 기술**: 디스크 상의 이벤트 로그 삭제 공격 상황에 직면하여, 휘발성 메모리 덤프의 감사 프로세스 영역을 카빙 파싱하여 잃어버린 감사 증적을 입증하는 능력을 배양합니다.
