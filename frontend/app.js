const connectButton = document.getElementById("connect-wallet");
const chatbox = document.getElementById("chatbox");
const sendButton = document.getElementById("send-btn");
const messageInput = document.getElementById("message-input");
const messagesDiv = document.getElementById("messages");

let userAddress = null;

// 메타마스크 로그인 처리
connectButton.addEventListener("click", async () => {
  if (window.ethereum) {
    try {
      await window.ethereum.request({ method: "eth_requestAccounts" });
      const provider = new ethers.providers.Web3Provider(window.ethereum); // Web3Provider 사용
      const signer = provider.getSigner();
      userAddress = await signer.getAddress();
      console.log("연결된 지갑 주소:", userAddress);
      
      // 로그인 후 버튼 텍스트 변경
      connectButton.textContent = "채팅 시작";
      
      // 채팅창 표시
      chatbox.style.display = "block";
      console.log("채팅창을 보이게 설정했습니다.");  // 디버깅 추가

    } catch (error) {
      console.error("메타마스크 연결 실패:", error);
    }
  } else {
    alert("메타마스크가 설치되어 있지 않습니다.");
  }
});

// 메시지 전송 처리
sendButton.addEventListener("click", () => {
  const message = messageInput.value;
  if (message.trim() !== "") {
    addMessage("User", message);
    messageInput.value = ""; // 입력창 초기화
    // 여기에 GPT API 연동을 할 수 있어
    addMessage("AI", "AI의 답변"); // 임시로 AI 응답
  }
});

// 메시지 화면에 추가
function addMessage(sender, message) {
  const messageElement = document.createElement("div");
  messageElement.textContent = `${sender}: ${message}`;
  messagesDiv.appendChild(messageElement);
  messagesDiv.scrollTop = messagesDiv.scrollHeight; // 스크롤을 항상 최신 메시지로 이동
}
