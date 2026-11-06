// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title AgeVerificationContract
 * @dev 18歳以上のユーザーを年齢確認するスマートコントラクト
 * @notice マイナンバーカード検証はアプリ側で行い、このコントラクトではNFT発行と確認のみ実施
 */

contract AgeVerificationContract {
    // =====================
    // ストレージ変数
    // =====================
    
    /// @dev 政府公開鍵（ECDSA P-256, HEX形式）
    bytes public governmentPublicKey;
    
    /// @dev ユーザーアドレスがNFTを保有しているか
    mapping(address => bool) public ageVerifiedNFT;
    
    /// @dev 管理者アドレス
    address public admin;
    
    /// @dev 年齢確認手数料（wei単位、初期値: 0.001 ETH）
    uint256 public verificationFee = 0.001 ether;
    
    /// @dev 手数料の総収益
    uint256 public totalFeeCollected;
    
    /// @dev NFT発行履歴
    mapping(address => uint256) public verificationTimestamp;
    
    // =====================
    // イベント
    // =====================
    
    /// @notice 年齢確認NFT発行時に発火
    event AgeVerificationIssued(
        address indexed user,
        uint256 timestamp,
        bytes32 transactionHash
    );
    
    /// @notice 政府公開鍵更新時に発火
    event GovernmentPublicKeyUpdated(
        bytes newKey,
        uint256 timestamp
    );
    
    /// @notice 手数料更新時に発火
    event VerificationFeeUpdated(
        uint256 newFee,
        uint256 timestamp
    );
    
    /// @notice 手数料の管理者への払い出し時に発火
    event FeesWithdrawn(
        address indexed recipient,
        uint256 amount,
        uint256 timestamp
    );
    
    // =====================
    // コンストラクタ
    // =====================
    
    /**
     * @dev コントラクト初期化
     * @param initialPublicKey 初期の政府公開鍵
     */
    constructor(bytes memory initialPublicKey) {
        admin = msg.sender;
        governmentPublicKey = initialPublicKey;
    }
    
    // =====================
    // 修飾子（Modifier）
    // =====================
    
    /// @notice 管理者のみが実行可能
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this function");
        _;
    }
    
    // =====================
    // 管理者用関数
    // =====================
    
    /**
     * @dev 政府公開鍵を更新（管理者のみ）
     * @param newPublicKey 新しい公開鍵
     */
    function setGovernmentPublicKey(bytes memory newPublicKey) public onlyAdmin {
        require(newPublicKey.length > 0, "Public key cannot be empty");
        governmentPublicKey = newPublicKey;
        
        emit GovernmentPublicKeyUpdated(newPublicKey, block.timestamp);
    }
    
    /**
     * @dev 手数料を更新（管理者のみ）
     * @param newFee 新しい手数料（wei単位）
     */
    function setVerificationFee(uint256 newFee) public onlyAdmin {
        verificationFee = newFee;
        
        emit VerificationFeeUpdated(newFee, block.timestamp);
    }
    
    /**
     * @dev 手数料を引き出す（管理者のみ）
     * @param amount 引き出し額
     */
    function withdrawFees(uint256 amount) public onlyAdmin {
        require(amount <= address(this).balance, "Insufficient contract balance");
        
        payable(admin).transfer(amount);
        totalFeeCollected -= amount;
        
        emit FeesWithdrawn(admin, amount, block.timestamp);
    }
    
    // =====================
    // ユーザー用関数
    // =====================
    
    /**
     * @dev 公開鍵を取得（アプリ側で署名検証に使用）
     * @return 政府公開鍵
     */
    function getGovernmentPublicKey() public view returns (bytes memory) {
        return governmentPublicKey;
    }
    
    /**
     * @dev 年齢確認NFTを発行
     * @notice アプリ側で年齢確認済みの場合のみ呼び出し
     * @return 発行成功時 true
     */
    function issueAgeVerificationNFT() public payable returns (bool) {
        // 手数料チェック
        require(msg.value >= verificationFee, "Insufficient payment");
        
        // 既に発行済みかチェック（1ユーザー1回のみ）
        require(!ageVerifiedNFT[msg.sender], "Already verified");
        
        // NFT発行（フラグをtrueに設定）
        ageVerifiedNFT[msg.sender] = true;
        verificationTimestamp[msg.sender] = block.timestamp;
        totalFeeCollected += msg.value;
        
        // イベント発火
        emit AgeVerificationIssued(
            msg.sender,
            block.timestamp,
            blockhash(block.number - 1)
        );
        
        return true;
    }
    
    /**
     * @dev 年齢確認NFTを検証（SaaS企業が呼び出し）
     * @param userAddress 確認対象ユーザーのアドレス
     * @return ユーザーがNFTを保有している場合 true
     */
    function verifyAgeVerification(address userAddress) public view returns (bool) {
        require(userAddress != address(0), "Invalid address");
        return ageVerifiedNFT[userAddress];
    }
    
    /**
     * @dev ユーザーの年齢確認状態を取得
     * @param userAddress 確認対象ユーザーのアドレス
     * @return isVerified: NFT保有状態
     * @return verificationTime: 確認のタイムスタンプ
     */
    function getUserVerificationStatus(address userAddress) 
        public 
        view 
        returns (bool isVerified, uint256 verificationTime) 
    {
        isVerified = ageVerifiedNFT[userAddress];
        verificationTime = verificationTimestamp[userAddress];
        return (isVerified, verificationTime);
    }
    
    /**
     * @dev NFTを取り消す（管理者が不正を検出した場合など）
     * @param userAddress 取り消し対象ユーザー
     */
    function revokeAgeVerification(address userAddress) public onlyAdmin {
        require(ageVerifiedNFT[userAddress], "User is not verified");
        ageVerifiedNFT[userAddress] = false;
        verificationTimestamp[userAddress] = 0;
    }
    
    // =====================
    // Fallback関数
    // =====================
    
    /// @notice 誤ったEther送金を受け取った場合
    receive() external payable {
        revert("Direct payment not allowed. Use issueAgeVerificationNFT()");
    }
}
