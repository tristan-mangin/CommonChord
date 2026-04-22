from rest_framework import serializers
from .models import Repository, Commit

class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = [
            'hash', 
            'parent_hash',
            'blob_hash',
            'message',
            'timestamp',
        ]

class RepositorySerializer(serializers.ModelSerializer):
    '''
    for reads - includes full nested commit history and derived path
    used for GET /api/repos/ and GET /api/repos/{id}/
    '''
    commits = CommitSerializer(many=True, read_only=True)

    class Meta:
        model = Repository
        fields = [
            'id',
            'name',
            'path',
            'created_at',
            'commits',
        ]

class RepositoryCreateSerializer(serializers.ModelSerializer):
    '''
    for writes - client only provides a name and view derives path from using BVCSClient.repo_path_for()
    used for POST /api/repos/
    '''
    class Meta: 
        model = Repository
        fields = ['name']