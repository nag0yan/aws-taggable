import boto3
import json
from botocore.exceptions import ClientError
import logging

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_all_aws_services():
    """利用可能なすべてのAWSサービス名を取得"""
    session = boto3.Session()
    return session.get_available_services()

def get_service_actions(service_name):
    """指定されたサービスで利用可能なすべてのAPIアクションを取得"""
    try:
        # サービスのクライアントを作成
        client = boto3.client(service_name)
        
        # サービスモデルからオペレーション（アクション）を取得
        operations = client.meta.service_model.operation_names
        
        return sorted(operations)
    except Exception as e:
        logger.warning(f"Error getting actions for service {service_name}: {str(e)}")
        return []

def save_actions_to_file(actions_dict, filename="aws_actions.json"):
    """アクションリストをJSONファイルとして保存"""
    try:
        with open(filename, 'w') as f:
            json.dump(actions_dict, f, indent=2)
        logger.info(f"Actions saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving actions to file: {str(e)}")

def main():
    # 結果を格納する辞書
    all_actions = {}
    
    # すべてのサービスを取得
    services = get_all_aws_services()
    logger.info(f"Found {len(services)} AWS services")
    
    # 各サービスのアクションを取得
    for service in services:
        logger.info(f"Getting actions for {service}")
        actions = get_service_actions(service)
        
        if actions:
            all_actions[service] = {
                "count": len(actions),
                "actions": actions
            }
    
    # 結果を保存
    save_actions_to_file(all_actions)
    
    # 統計情報を表示
    total_actions = sum(data["count"] for data in all_actions.values())
    logger.info(f"Total number of actions across all services: {total_actions}")
    logger.info(f"Number of services with actions: {len(all_actions)}")

if __name__ == "__main__":
    main()
